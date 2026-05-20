import uuid
from pathlib import Path
from typing import Optional, Dict, Any
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from project_manager import ProjectManager
from module_wizards import DEFAULT_INSTITUTIONAL_INTAKE, BP_WIZARD_SECTIONS, MODULE_SETUP_TIMES
from institutional_bp_engine import clean_intake, to_legacy_build_config
from institutional_excel_builder import build_institutional_bp_excel
from institutional_qoe_engine import build_institutional_qoe
from institutional_restructuring_engine import build_restructuring_pack
from institutional_deck_builder import build_institutional_im_deck

try:
    from extractor import extract_document
    from financial_normalizer import normalize_extracted_payload
    from quality_checks import run_quality_checks
    EXTRACTION_AVAILABLE = True
except Exception as e:
    EXTRACTION_AVAILABLE = False
    EXTRACTION_ERROR = str(e)

try:
    from build import build_model
    LEGACY_BP_AVAILABLE = True
except Exception as e:
    LEGACY_BP_AVAILABLE = False
    LEGACY_BP_ERROR = str(e)

BASE_DIR = Path(__file__).resolve().parent
pm = ProjectManager(BASE_DIR)

app = FastAPI(title="MG Advisory Elite Institutional SaaS", version="5.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

VALID_KEYS = {"JRC-MATEO-2025", "JRC-JAUFRE-2025", "JRC-OZAN-2025", "JRC-DEV-LOCAL", "MG-ACCESS-2025", "BP-ELITE-2025"}

class LoginRequest(BaseModel):
    license_key: str

class ProjectCreate(BaseModel):
    license_key: str
    name: str
    company_name: str = "Target Company"
    sector: str = "General"
    currency: str = "EUR"
    deal_type: str = "M&A"

class IntakeRequest(BaseModel):
    license_key: str
    project_id: str
    intake: Dict[str, Any]

class GenerateRequest(BaseModel):
    license_key: str
    project_id: Optional[str] = None
    intake: Optional[Dict[str, Any]] = None
    use_legacy_bp: bool = True

def check_license(key: str):
    if not key or (key not in VALID_KEYS and not key.startswith("JRC-")):
        raise HTTPException(status_code=401, detail="Invalid license key")

def get_project(project_id: str, license_key: str):
    try:
        return pm.get_project(project_id, license_key)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")
    except PermissionError:
        raise HTTPException(status_code=403, detail="Access denied")

def project_intake(project):
    x = dict(DEFAULT_INSTITUTIONAL_INTAKE)
    x.update(project.intake or {})
    x["company_name"] = project.company_name
    x["currency"] = project.currency
    x["sector"] = project.sector
    x["deal_type"] = project.deal_type
    return clean_intake(x)

@app.get("/", response_class=HTMLResponse)
def index():
    path = BASE_DIR / "index.html"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "<h1>MG Advisory Elite Institutional SaaS</h1>"

@app.get("/app", response_class=HTMLResponse)
def app_page():
    return index()

@app.get("/health")
def health():
    return {
        "ok": True,
        "service": "MG Advisory Elite Institutional SaaS",
        "version": "5.0",
        "extraction_available": EXTRACTION_AVAILABLE,
        "legacy_bp_available": LEGACY_BP_AVAILABLE,
        "modules": ["projects", "bp", "qoe", "deck", "restructuring"]
    }

@app.post("/api/auth/login")
def login(payload: LoginRequest):
    check_license(payload.license_key)
    return {"ok": True, "license": payload.license_key}

@app.get("/api/wizards")
def wizards():
    return {
        "bp_sections": BP_WIZARD_SECTIONS,
        "default_intake": DEFAULT_INSTITUTIONAL_INTAKE,
        "setup_times": MODULE_SETUP_TIMES
    }

@app.post("/api/projects")
def create_project(payload: ProjectCreate):
    check_license(payload.license_key)
    project = pm.create_project(payload.license_key, payload.name, payload.company_name, payload.sector, payload.currency, payload.deal_type)
    project.intake = dict(DEFAULT_INSTITUTIONAL_INTAKE)
    project.intake.update({"company_name": project.company_name, "sector": project.sector, "currency": project.currency, "deal_type": project.deal_type})
    project = pm.set_intake(project.project_id, payload.license_key, project.intake)
    return {"ok": True, "project": project.model_dump()}

@app.get("/api/projects")
def list_projects(license_key: str):
    check_license(license_key)
    return {"ok": True, "projects": [p.model_dump() for p in pm.list_projects(license_key)]}

@app.get("/api/projects/{project_id}")
def read_project(project_id: str, license_key: str):
    check_license(license_key)
    return {"ok": True, "project": get_project(project_id, license_key).model_dump()}

@app.post("/api/projects/{project_id}/intake")
def save_intake(project_id: str, payload: IntakeRequest):
    check_license(payload.license_key)
    project = get_project(project_id, payload.license_key)
    intake = dict(project.intake or {})
    intake.update(payload.intake or {})
    intake = clean_intake(intake)
    project = pm.set_intake(project_id, payload.license_key, intake)
    return {"ok": True, "project": project.model_dump(), "intake": intake}

@app.post("/api/projects/{project_id}/upload")
async def upload(project_id: str, license_key: str = Form(...), category: str = Form("financials"), file: UploadFile = File(...)):
    check_license(license_key)
    project = get_project(project_id, license_key)
    doc = pm.add_document(project_id, license_key, file.filename, await file.read(), category)

    if EXTRACTION_AVAILABLE:
        extracted = extract_document(doc.path)
        financials = normalize_extracted_payload(extracted, company_name=project.company_name)
        financials = run_quality_checks(financials)
        pm.set_financials(project_id, license_key, financials.model_dump())
        return {"ok": True, "document": doc.model_dump(), "financials": financials.model_dump()}
    return {"ok": True, "document": doc.model_dump(), "warning": f"Extraction unavailable: {globals().get('EXTRACTION_ERROR', '')}"}

@app.post("/api/projects/{project_id}/generate-bp")
def generate_bp(project_id: str, payload: GenerateRequest):
    check_license(payload.license_key)
    project = get_project(project_id, payload.license_key)
    if payload.intake:
        project = pm.set_intake(project_id, payload.license_key, clean_intake({**(project.intake or {}), **payload.intake}))
    intake = project_intake(project)

    file_id = str(uuid.uuid4())
    safe = project.company_name.replace(" ", "_").replace("/", "_")

    # Primary output: institutional BP Excel
    institutional_path = pm.outputs_dir / f"{file_id}_{safe}_Detailed_BP_Institutional.xlsx"
    build_institutional_bp_excel(intake, str(institutional_path))
    project = pm.add_output(project_id, payload.license_key, "bp_model", str(institutional_path))

    # Optional legacy detailed model if existing build.py is available
    if payload.use_legacy_bp and LEGACY_BP_AVAILABLE:
        try:
            legacy_path = pm.outputs_dir / f"{file_id}_{safe}_Legacy_Detailed_BP.xlsx"
            build_model(to_legacy_build_config(intake), str(legacy_path))
            project = pm.add_output(project_id, payload.license_key, "bp_legacy_model", str(legacy_path))
        except Exception:
            pass

    return {"ok": True, "file_id": file_id, "filename": institutional_path.name, "project": project.model_dump()}

@app.post("/api/projects/{project_id}/generate-qoe")
def generate_qoe(project_id: str, payload: GenerateRequest):
    check_license(payload.license_key)
    project = get_project(project_id, payload.license_key)
    intake = project_intake(project)
    file_id = str(uuid.uuid4())
    safe = project.company_name.replace(" ", "_").replace("/", "_")
    path = pm.outputs_dir / f"{file_id}_{safe}_QoE_Pack_Institutional.xlsx"
    build_institutional_qoe(intake, project.extracted_financials or {}, str(path))
    project = pm.add_output(project_id, payload.license_key, "qoe_pack", str(path))
    return {"ok": True, "file_id": file_id, "filename": path.name, "project": project.model_dump()}

@app.post("/api/projects/{project_id}/generate-restructuring")
def generate_restructuring(project_id: str, payload: GenerateRequest):
    check_license(payload.license_key)
    project = get_project(project_id, payload.license_key)
    intake = project_intake(project)
    file_id = str(uuid.uuid4())
    safe = project.company_name.replace(" ", "_").replace("/", "_")
    path = pm.outputs_dir / f"{file_id}_{safe}_Restructuring_Pack.xlsx"
    build_restructuring_pack(intake, str(path))
    project = pm.add_output(project_id, payload.license_key, "restructuring_pack", str(path))
    return {"ok": True, "file_id": file_id, "filename": path.name, "project": project.model_dump()}

@app.post("/api/projects/{project_id}/generate-deck")
def generate_deck(project_id: str, payload: GenerateRequest):
    check_license(payload.license_key)
    project = get_project(project_id, payload.license_key)
    if payload.intake:
        project = pm.set_intake(project_id, payload.license_key, clean_intake({**(project.intake or {}), **payload.intake}))
    intake = project_intake(project)
    file_id = str(uuid.uuid4())
    safe = project.company_name.replace(" ", "_").replace("/", "_")
    path = pm.outputs_dir / f"{file_id}_{safe}_Investment_Memorandum.pptx"
    build_institutional_im_deck(project.model_dump(), intake, str(path))
    project = pm.add_output(project_id, payload.license_key, "im_deck", str(path))
    return {"ok": True, "file_id": file_id, "filename": path.name, "project": project.model_dump()}

@app.post("/api/projects/{project_id}/generate-all")
def generate_all(project_id: str, payload: GenerateRequest):
    bp = generate_bp(project_id, payload)
    qoe = generate_qoe(project_id, payload)
    restructuring = generate_restructuring(project_id, payload)
    deck = generate_deck(project_id, payload)
    return {"ok": True, "bp": bp, "qoe": qoe, "restructuring": restructuring, "deck": deck}

@app.get("/api/projects/{project_id}/download/{output_type}")
def download_project_output(project_id: str, output_type: str, license_key: str):
    check_license(license_key)
    path = pm.get_output_path(project_id, license_key, output_type)
    if not path:
        raise HTTPException(status_code=404, detail="Output not found")
    return FileResponse(str(path), filename=path.name)

# Legacy compatibility
@app.post("/api/generate")
def legacy_generate(payload: GenerateRequest):
    check_license(payload.license_key)
    if payload.project_id:
        return generate_bp(payload.project_id, payload)
    project = pm.create_project(payload.license_key, "Quick BP", "Target Company")
    return generate_bp(project.project_id, GenerateRequest(license_key=payload.license_key, project_id=project.project_id, intake=payload.intake))

@app.post("/api/generate_deck")
def legacy_deck(payload: GenerateRequest):
    check_license(payload.license_key)
    if payload.project_id:
        return generate_deck(payload.project_id, payload)
    project = pm.create_project(payload.license_key, "Quick Deck", "Target Company")
    return generate_deck(project.project_id, GenerateRequest(license_key=payload.license_key, project_id=project.project_id, intake=payload.intake))

@app.get("/api/download/{file_id}")
def download_legacy(file_id: str):
    for p in pm.outputs_dir.glob(f"{file_id}_*"):
        return FileResponse(str(p), filename=p.name)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/api/download_deck/{file_id}")
def download_deck_legacy(file_id: str):
    return download_legacy(file_id)
