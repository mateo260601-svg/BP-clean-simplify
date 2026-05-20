import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from extraction_core import extract_document
    EXTRACTION_AVAILABLE = True
except Exception as e:
    EXTRACTION_AVAILABLE = False
    EXTRACTION_ERROR = str(e)

try:
    from claude_client import get_claude_status
    from ai_financial_extractor import enhance_extraction_with_claude
    CLAUDE_AVAILABLE = True
except Exception as e:
    CLAUDE_AVAILABLE = False
    CLAUDE_ERROR = str(e)
    def get_claude_status():
        return {"configured": False, "error": CLAUDE_ERROR}

from historical_accounts_engine import normalize_historical_accounts, merge_historical_into_intake
from institutional_debt_engine_v12 import debt_library_payload, default_debt_stack_for_saas
from institutional_formula_model_builder_v12 import build_v12_formula_model


app = FastAPI(title="MG Advisory Institutional BP + Debt Engine V12", version="12.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / "data"
PROJECTS_DIR = DATA_DIR / "projects"
OUTPUTS_DIR = BASE_DIR / "outputs"
UPLOADS_DIR = BASE_DIR / "uploads"
for d in [DATA_DIR, PROJECTS_DIR, OUTPUTS_DIR, UPLOADS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

VALID_LICENSES = {
    "JRC-MATEO-2025": {"user": "Mateo Girard", "expires": "2027-12-31"},
    "JRC-JAUFRE-2025": {"user": "Jaufre Rouanet", "expires": "2027-12-31"},
    "JRC-OZAN-2025": {"user": "Ozan OK", "expires": "2027-12-31"},
    "JRC-DEV-LOCAL": {"user": "Developer", "expires": "2099-12-31"},
    "MG-ACCESS-2025": {"user": "MG Advisory", "expires": "2027-12-31"},
    "BP-ELITE-2025": {"user": "MG Advisory", "expires": "2027-12-31"},
}


class LoginRequest(BaseModel):
    license_key: str


class ProjectCreate(BaseModel):
    license_key: str
    name: str = "New Investment Project"
    company_name: str = "Target Company"
    sector: str = "Industrial / Manufacturing"
    currency: str = "EUR"
    deal_type: str = "M&A"


class IntakeRequest(BaseModel):
    license_key: str
    project_id: str
    intake: Dict[str, Any] = {}


class GenerateRequest(BaseModel):
    license_key: str
    project_id: Optional[str] = None
    intake: Optional[Dict[str, Any]] = None
    company_name: str = "Target Company"


def check_license(key: str):
    k = (key or "").strip().upper()
    if k not in VALID_LICENSES and not k.startswith("JRC-"):
        raise HTTPException(status_code=401, detail="Invalid license key")
    return VALID_LICENSES.get(k, {"user": "JRC User"})


def default_intake(company_name="Target Company", currency="EUR", sector="Industrial / Manufacturing", deal_type="M&A"):
    return {
        "company_name": company_name,
        "currency": currency,
        "sector": sector,
        "deal_type": deal_type,
        "start_year": 2026,
        "forecast_years": 5,
        "revenue": 202000,
        "revenue_growth": 0.073,
        "gross_margin": 0.391,
        "ebitda_margin": 0.229,
        "tax_rate": 0.25,
        "cash": 18700,
        "debt": 201000,
        "dso": 55,
        "dio": 40,
        "dpo": 55,
        "maintenance_capex_pct_revenue": 0.055,
        "debt_stack": default_debt_stack_for_saas(),
    }


def project_file(project_id):
    return PROJECTS_DIR / project_id / "project.json"


def save_project(project):
    project["updated_at"] = datetime.utcnow().isoformat()
    folder = PROJECTS_DIR / project["project_id"]
    folder.mkdir(parents=True, exist_ok=True)
    project_file(project["project_id"]).write_text(json.dumps(project, indent=2), encoding="utf-8")
    return project


def load_project(project_id, license_key=None):
    path = project_file(project_id)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Project not found")
    project = json.loads(path.read_text(encoding="utf-8"))
    if license_key and project.get("license_key") != license_key:
        raise HTTPException(status_code=403, detail="Access denied")
    return project


@app.get("/", response_class=HTMLResponse)
def index():
    path = BASE_DIR / "index.html"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return "<h1>MG Advisory Debt Engine V12 is online</h1>"


@app.get("/app", response_class=HTMLResponse)
def app_page():
    return index()


@app.get("/health")
def health():
    debt_payload = debt_library_payload()
    return {
        "ok": True,
        "version": "12.0",
        "institutional_debt_engine_v12": True,
        "debt_types": len(debt_payload["debt_types"]),
        "max_tranches": 60,
        "extraction_available": EXTRACTION_AVAILABLE,
        "extraction_error": None if EXTRACTION_AVAILABLE else EXTRACTION_ERROR,
        "claude": get_claude_status(),
    }


@app.get("/api/debt/library")
def debt_library():
    return {"ok": True, **debt_library_payload()}


@app.post("/api/auth/login")
def login(payload: LoginRequest):
    user = check_license(payload.license_key)
    return {"ok": True, "license": payload.license_key, "user": user["user"]}


@app.get("/api/wizards")
def wizards():
    return {
        "ok": True,
        "default_intake": default_intake(),
        "debt": debt_library_payload(),
    }


@app.post("/api/projects")
def create_project(payload: ProjectCreate):
    check_license(payload.license_key)
    project = {
        "project_id": str(uuid.uuid4()),
        "license_key": payload.license_key,
        "name": payload.name,
        "company_name": payload.company_name,
        "sector": payload.sector,
        "currency": payload.currency,
        "deal_type": payload.deal_type,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
        "documents": [],
        "extractions": [],
        "historical": {"periods": [], "evidence": [], "warnings": []},
        "intake": default_intake(payload.company_name, payload.currency, payload.sector, payload.deal_type),
        "outputs": {},
    }
    save_project(project)
    return {"ok": True, "project": project}


@app.get("/api/projects")
def list_projects(license_key: str):
    check_license(license_key)
    projects = []
    for fp in PROJECTS_DIR.glob("*/project.json"):
        try:
            p = json.loads(fp.read_text(encoding="utf-8"))
            if p.get("license_key") == license_key:
                projects.append(p)
        except Exception:
            pass
    return {"ok": True, "projects": sorted(projects, key=lambda x: x.get("updated_at", ""), reverse=True)}


@app.get("/api/projects/{project_id}")
def get_project(project_id: str, license_key: str):
    check_license(license_key)
    return {"ok": True, "project": load_project(project_id, license_key)}


@app.post("/api/projects/{project_id}/upload")
async def upload_project_file(project_id: str, license_key: str = Form(...), category: str = Form("financials"), file: UploadFile = File(...), use_ai: bool = Form(True)):
    check_license(license_key)
    project = load_project(project_id, license_key)

    file_id = str(uuid.uuid4())
    safe = file.filename.replace("/", "_").replace("\\", "_")
    folder = PROJECTS_DIR / project_id / "documents"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{file_id}_{safe}"
    path.write_bytes(await file.read())

    if not EXTRACTION_AVAILABLE:
        raise HTTPException(status_code=500, detail=f"Extraction unavailable: {EXTRACTION_ERROR}")

    extraction = extract_document(str(path))
    if use_ai and CLAUDE_AVAILABLE:
        extraction = enhance_extraction_with_claude(extraction)

    project["documents"].append({
        "file_id": file_id,
        "filename": safe,
        "path": str(path),
        "category": category,
        "uploaded_at": datetime.utcnow().isoformat(),
    })
    project["extractions"].append(extraction)

    historical = normalize_historical_accounts(project["extractions"])
    project["historical"] = historical
    project["intake"] = merge_historical_into_intake(project.get("intake") or {}, historical)
    project["intake"].setdefault("debt_stack", default_debt_stack_for_saas())

    save_project(project)
    return {
        "ok": True,
        "file_id": file_id,
        "project": project,
        "historical": historical,
        "suggested_intake": project["intake"],
        "warnings": historical.get("warnings", []),
    }


@app.post("/api/projects/{project_id}/intake")
def save_intake(project_id: str, payload: IntakeRequest):
    check_license(payload.license_key)
    project = load_project(project_id, payload.license_key)
    project["intake"].update(payload.intake or {})
    project["intake"].setdefault("debt_stack", default_debt_stack_for_saas())
    save_project(project)
    return {"ok": True, "project": project, "intake": project["intake"]}


@app.post("/api/projects/{project_id}/generate-bp")
def generate_project_bp(project_id: str, payload: GenerateRequest):
    check_license(payload.license_key)
    project = load_project(project_id, payload.license_key)

    intake = dict(project.get("intake") or {})
    if payload.intake:
        intake.update(payload.intake)
    intake.setdefault("debt_stack", default_debt_stack_for_saas())

    historical = project.get("historical") or {"periods": [], "evidence": [], "warnings": []}
    file_id = str(uuid.uuid4())
    safe = project.get("company_name", "Company").replace(" ", "_").replace("/", "_")
    output = OUTPUTS_DIR / f"{file_id}_{safe}_Institutional_BP_Debt_Engine_V12.xlsx"

    build_v12_formula_model(intake, historical, str(output))

    project["intake"] = intake
    project["outputs"]["bp_model"] = str(output)
    save_project(project)
    return {"ok": True, "file_id": file_id, "filename": output.name, "project": project}


@app.post("/api/generate")
def legacy_generate(payload: GenerateRequest):
    check_license(payload.license_key)
    intake = default_intake(payload.company_name)
    if payload.intake:
        intake.update(payload.intake)
    historical = {"periods": [], "evidence": [], "warnings": ["No historical accounts uploaded in legacy mode"]}
    file_id = str(uuid.uuid4())
    safe = intake.get("company_name", "Company").replace(" ", "_").replace("/", "_")
    output = OUTPUTS_DIR / f"{file_id}_{safe}_Institutional_BP_Debt_Engine_V12.xlsx"
    build_v12_formula_model(intake, historical, str(output))
    return {"ok": True, "file_id": file_id, "filename": output.name}


@app.get("/api/projects/{project_id}/download/{output_type}")
def download_project(project_id: str, output_type: str, license_key: str):
    check_license(license_key)
    project = load_project(project_id, license_key)
    path = project.get("outputs", {}).get(output_type)
    if not path or not Path(path).exists():
        raise HTTPException(status_code=404, detail="Output not found")
    return FileResponse(path, filename=Path(path).name)


@app.get("/api/download/{file_id}")
def download_legacy(file_id: str):
    for p in OUTPUTS_DIR.glob(f"{file_id}_*"):
        return FileResponse(str(p), filename=p.name)
    raise HTTPException(status_code=404, detail="File not found")
