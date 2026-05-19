import os, json, uuid, tempfile
from datetime import datetime
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="BP Generator — MG Advisory")

VALID_LICENSES = {
    "JRC-MATEO-2025":  {"user": "Mateo Girard",  "expires": "2027-12-31"},
    "JRC-JAUFRE-2025": {"user": "Jaufre",         "expires": "2027-12-31"},
    "JRC-OZAN-2025":   {"user": "Ozan",           "expires": "2027-12-31"},
    "JRC-DEV-LOCAL":   {"user": "Developer",      "expires": "2099-12-31"},
}

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class LoginRequest(BaseModel):
    license_key: str

class GenerateRequest(BaseModel):
    license_key: str
    config: dict

def _check_license(key: str):
    k = key.strip().upper()
    if k not in VALID_LICENSES:
        raise HTTPException(status_code=401, detail="Invalid license key")
    if datetime.strptime(VALID_LICENSES[k]["expires"], "%Y-%m-%d") < datetime.now():
        raise HTTPException(status_code=401, detail="License expired")
    return VALID_LICENSES[k]

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "4.0"}

@app.post("/api/auth/login")
def login(req: LoginRequest):
    info = _check_license(req.license_key)
    return {"success": True, "user": info["user"], "license_key": req.license_key.strip().upper()}

@app.post("/api/import")
async def import_financials(
    file: UploadFile = File(...),
    license_key: str = Form(...),
):
    """
    LLM-powered financial statement import.
    Claude reads the file and extracts structured historical data.
    """
    _check_license(license_key)

    allowed = {"xlsx","xls","xlsm","csv","pdf"}
    ext = file.filename.rsplit(".", 1)[-1].lower()
    if ext not in allowed:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: .{ext}")

    file_bytes = await file.read()
    if len(file_bytes) > 20 * 1024 * 1024:  # 20MB limit
        raise HTTPException(status_code=400, detail="File too large (max 20MB)")

    try:
        from extractor_llm import extract_financials_llm
        result = await extract_financials_llm(file_bytes, file.filename)
        return JSONResponse(content=result)
    except Exception as e:
        # Fallback to keyword extractor if LLM fails
        try:
            from extractor_v2 import extract_financials
            result = extract_financials(file_bytes, file.filename)
            result["fallback"] = True
            result["fallback_reason"] = str(e)
            return JSONResponse(content=result)
        except Exception as e2:
            raise HTTPException(status_code=500, detail=f"Extraction failed: {e2}")

@app.post("/api/generate")
def generate(req: GenerateRequest):
    _check_license(req.license_key)
    try:
        from build import build_model
        tmp     = tempfile.mktemp(suffix=".xlsx")
        build_model(req.config, tmp)
        file_id = str(uuid.uuid4())
        dest    = os.path.join(tempfile.gettempdir(), f"bp_{file_id}.xlsx")
        os.rename(tmp, dest)
        company = req.config.get("company_name","BP").replace(" ","_")
        return {"success": True, "file_id": file_id, "filename": f"{company}_BP.xlsx"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{file_id}")
def download(file_id: str):
    path = os.path.join(tempfile.gettempdir(), f"bp_{file_id}.xlsx")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File expired or not found")
    return FileResponse(path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="BP_Generator.xlsx")

@app.get("/")
def root():
    index = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index) if os.path.exists(index) else HTMLResponse("<h2>BP Generator</h2>")

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    index = os.path.join(BASE_DIR, "index.html")
    return FileResponse(index) if os.path.exists(index) else HTTPException(status_code=404)
