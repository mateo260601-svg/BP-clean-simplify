import uuid
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from extractor import extract_document
from financial_normalizer import normalize_extracted_payload
from quality_checks import run_quality_checks
from excel_model_builder import build_excel_model
from deck_generator import generate_deck
from financial_schema import NormalizedFinancials

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app = FastAPI(title="MG Advisory Investment Banking Suite", version="3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

LAST_FINANCIALS: Dict[str, NormalizedFinancials] = {}
OUTPUT_FILES: Dict[str, Path] = {}

VALID_KEYS = {"JRC-MATEO-2025", "JRC-JAUFRE-2025", "JRC-OZAN-2025", "JRC-DEV-LOCAL", "MG-ACCESS-2025", "BP-ELITE-2025"}

class LoginRequest(BaseModel):
    license_key: str

class GenerateRequest(BaseModel):
    license_key: str
    company_name: str = "Target Company"
    config: Optional[Dict[str, Any]] = None
    extracted_payload: Optional[Dict[str, Any]] = None

def check_license(key: str):
    if key not in VALID_KEYS:
        raise HTTPException(status_code=401, detail="Invalid license key")

@app.get("/", response_class=HTMLResponse)
def index():
    index_path = BASE_DIR / "index.html"
    if index_path.exists():
        return index_path.read_text(encoding="utf-8")
    return "<h1>MG Advisory Investment Banking Suite</h1>"

@app.post("/api/auth/login")
def login(payload: LoginRequest):
    check_license(payload.license_key)
    return {"ok": True, "license": payload.license_key}

@app.post("/api/import")
async def import_file(license_key: str = Form(...), file: UploadFile = File(...)):
    check_license(license_key)
    file_id = str(uuid.uuid4())
    safe_name = file.filename.replace("/", "_").replace("\\", "_")
    path = UPLOAD_DIR / f"{file_id}_{safe_name}"
    path.write_bytes(await file.read())

    extracted = extract_document(str(path))
    financials = normalize_extracted_payload(extracted, company_name=safe_name.rsplit(".", 1)[0])
    financials = run_quality_checks(financials)
    LAST_FINANCIALS[license_key] = financials
    return {"ok": True, "file_id": file_id, "filename": safe_name, "financials": financials.model_dump()}

def fallback_financials(company_name: str = "Target Company") -> NormalizedFinancials:
    payload = {"source_type": "demo", "text": "FY2024 Revenue 202000000 EBITDA 42300000 Cash 18700000 Debt 201000000 Capex 11500000 Free Cash Flow 9500000"}
    return run_quality_checks(normalize_extracted_payload(payload, company_name=company_name))

@app.post("/api/generate")
def generate_excel(payload: GenerateRequest):
    check_license(payload.license_key)
    financials = LAST_FINANCIALS.get(payload.license_key) or fallback_financials(payload.company_name)
    file_id = str(uuid.uuid4())
    output = OUTPUT_DIR / f"{file_id}_MG_Advisory_Excel_Model.xlsx"
    build_excel_model(financials, str(output))
    OUTPUT_FILES[file_id] = output
    return {"ok": True, "file_id": file_id, "filename": output.name}

@app.post("/api/generate_deck")
def generate_im_deck(payload: GenerateRequest):
    check_license(payload.license_key)
    financials = LAST_FINANCIALS.get(payload.license_key) or fallback_financials(payload.company_name)
    file_id = str(uuid.uuid4())
    output = OUTPUT_DIR / f"{file_id}_MG_Advisory_IM_Deck.pptx"
    generate_deck(financials, str(output))
    OUTPUT_FILES[file_id] = output
    return {"ok": True, "file_id": file_id, "filename": output.name}

@app.get("/api/download/{file_id}")
def download(file_id: str):
    path = OUTPUT_FILES.get(file_id)
    if not path or not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(path), filename=path.name)

@app.get("/api/download_deck/{file_id}")
def download_deck(file_id: str):
    return download(file_id)

@app.get("/health")
def health():
    return {"ok": True, "service": "MG Advisory Investment Banking Suite"}
