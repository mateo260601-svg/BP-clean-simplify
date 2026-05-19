import os, io, json, uuid, tempfile
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="BP Generator")

# ── Auth ──────────────────────────────────────────────────────────────────────
VALID_LICENSES = {
    "JRC-MATEO-2025":  {"user": "Mateo Girard",          "expires": "2027-12-31"},
    "JRC-JAUFRE-2025": {"user": "Jaufre",                "expires": "2027-12-31"},
    "JRC-OZAN-2025":   {"user": "Ozan",                  "expires": "2027-12-31"},
    "JRC-DEV-LOCAL":   {"user": "Developer",             "expires": "2099-12-31"},
}

# ── Static files ───────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ── Models ─────────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    license_key: str

class GenerateRequest(BaseModel):
    license_key: str
    config: dict

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    return {"status": "ok", "version": "2.0"}

@app.post("/api/auth/login")
def login(req: LoginRequest):
    key = req.license_key.strip().upper()
    if key not in VALID_LICENSES:
        raise HTTPException(status_code=401, detail="Invalid license key")
    info = VALID_LICENSES[key]
    exp = datetime.strptime(info["expires"], "%Y-%m-%d")
    if exp < datetime.now():
        raise HTTPException(status_code=401, detail="License expired")
    return {"success": True, "user": info["user"], "license_key": key}

@app.post("/api/generate")
def generate(req: GenerateRequest):
    key = req.license_key.strip().upper()
    if key not in VALID_LICENSES:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        from build import build_model
        cfg = req.config
        tmp = tempfile.mktemp(suffix=".xlsx")
        build_model(cfg, tmp)
        file_id = str(uuid.uuid4())
        dest = os.path.join(tempfile.gettempdir(), f"bp_{file_id}.xlsx")
        os.rename(tmp, dest)
        company = cfg.get("company_name", "BP").replace(" ", "_")
        return {"success": True, "file_id": file_id, "filename": f"{company}_BP.xlsx"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/download/{file_id}")
def download(file_id: str):
    path = os.path.join(tempfile.gettempdir(), f"bp_{file_id}.xlsx")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found or expired")
    return FileResponse(
        path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="BP_Generator.xlsx"
    )

@app.get("/api/preview/{file_id}")
def preview(file_id: str):
    path = os.path.join(tempfile.gettempdir(), f"bp_{file_id}.xlsx")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File not found")
    try:
        from preview import extract_preview
        data = extract_preview(path)
        return JSONResponse(content=data)
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

# ── Serve frontend ─────────────────────────────────────────────────────────────
@app.get("/")
def root():
    index = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return HTMLResponse("<h2>BP Generator API running. Frontend not found.</h2>")

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    index = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    raise HTTPException(status_code=404, detail="Not found")
