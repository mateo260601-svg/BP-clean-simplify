import os, json, uuid, tempfile
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="BP Generator - MG Advisory", version="5.0 Investment Banking Suite")
# Corrected server.py: no dependency on missing formatters.py
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

VALID_LICENSES = {
    "JRC-MATEO-2025":  {"user": "Mateo Girard",   "expires": "2027-12-31"},
    "JRC-JAUFRE-2025": {"user": "Jaufre Rouanet", "expires": "2027-12-31"},
    "JRC-OZAN-2025":   {"user": "Ozan OK",        "expires": "2027-12-31"},
    "JRC-DEV-LOCAL":   {"user": "Developer",      "expires": "2099-12-31"},
}

BASE_DIR    = Path(__file__).parent.resolve()
OUTPUTS_DIR = BASE_DIR / "outputs"
DECKS_DIR = BASE_DIR / "decks"
OUTPUTS_DIR.mkdir(exist_ok=True)
DECKS_DIR.mkdir(exist_ok=True)
INDEX       = BASE_DIR / "index.html"

def _check_license(key):
    k = (key or "").strip().upper()
    if k not in VALID_LICENSES:
        raise HTTPException(status_code=401, detail="Invalid license key")
    if datetime.strptime(VALID_LICENSES[k]["expires"], "%Y-%m-%d") < datetime.now():
        raise HTTPException(status_code=401, detail="License expired")
    return VALID_LICENSES[k]

def _f(v, d=0.0):
    try: return float(v) if v is not None else d
    except: return d
def _i(v, d=0):
    try: return int(float(v)) if v is not None else d
    except: return d
def _s(v, d=""):
    return str(v) if v is not None else d

def _map_config(c):
    company  = c.get("company",  {}) if isinstance(c.get("company"),  dict) else {}
    revenue  = c.get("revenue",  {}) if isinstance(c.get("revenue"),  dict) else {}
    costs    = c.get("costs",    {}) if isinstance(c.get("costs"),    dict) else {}
    nwc      = c.get("nwc",      {}) if isinstance(c.get("nwc"),      dict) else {}
    capex    = c.get("capex",    {}) if isinstance(c.get("capex"),    dict) else {}
    debt     = c.get("debt",     {}) if isinstance(c.get("debt"),     dict) else {}
    tax      = c.get("tax",      {}) if isinstance(c.get("tax"),      dict) else {}

    flat = {
        "company_name":   _s(company.get("name") or c.get("company_name"), "Company"),
        "currency":       _s(company.get("currency") or c.get("currency"), "USD"),
        "business_type":  _s(company.get("sector") or c.get("business_type"), "industrial"),
        "n_years":        _i(revenue.get("projection_years") or c.get("n_years"), 5),
        "start_year":     _i(revenue.get("start_year") or c.get("start_year"), 2025),
        "actuals_months": _i(revenue.get("actuals_years", 0)) * 12 if revenue.get("actuals_years") else _i(c.get("actuals_months"), 0),
        "base_revenue":   _f(revenue.get("base_revenue") or c.get("base_revenue"), 50000),
        "revenue_growth": _f(revenue.get("volume_growth") or c.get("revenue_growth"), 0.05),
        "gross_margin":   _f(costs.get("gross_margin") or c.get("gross_margin"), 0.35),
        "ebitda_margin":  _f(costs.get("ebitda_margin") or c.get("ebitda_margin"), 0.20),
        "price_per_mt":   _f(revenue.get("price_per_unit") or c.get("price_per_mt"), 1050),
        "price_growth":   _f(revenue.get("price_growth") or c.get("price_growth"), 0.02),
        "capacity_mt":    _f(revenue.get("capacity_mt") or c.get("capacity_mt"), 220000),
        "volume_mt":      _f(revenue.get("base_volume") or c.get("volume_mt"), 180000),
        "cogs_pct":       _f(costs.get("cogs_pct") or c.get("cogs_pct"), 0.65),
        "sga_pct":        _f(costs.get("sga_pct") or c.get("sga_pct"), 0.10),
        "inflation":      _f(c.get("inflation"), 0.025),
        "dso":  _f(nwc.get("dso")  or c.get("dso"),  60),
        "dio":  _f(nwc.get("dio")  or c.get("dio"),  30),
        "dio_rm": _f(nwc.get("dio_rm") or c.get("dio_rm"), 30),
        "dpo":  _f(nwc.get("dpo")  or c.get("dpo"),  45),
        "capex": {
            "opening_ppe": _f(capex.get("opening_ppe") or c.get("opening_ppe"), 85000),
            "maint_capex": _f(capex.get("maintenance") or capex.get("maint_capex") or c.get("maint_capex"), 2000),
            "expan_capex": _f(capex.get("expansion")   or capex.get("expan_capex") or c.get("expan_capex"), 5000),
            "useful_life": _i(capex.get("useful_life") or c.get("useful_life"), 20),
        },
        "tax_rate":    _f(tax.get("rate") or c.get("tax_rate"), 0.25),
        "opening_cash": _f(c.get("opening_cash"), 5000),
        "debt":     _map_debt(debt if debt else c.get("debt", {})),
        "scenarios": "all" if c.get("scenarios") == "all" else "base",
    }
    return flat

def _map_debt(d):
    if not d:
        return {"tranches": [], "total_debt": 0, "interest_rate": 0.07}
    tranches = []
    for t in (d.get("tranches") or []):
        if not isinstance(t, dict):
            continue
        amt = _f(t.get("amount"), 0)
        if amt <= 0:
            continue
        tranches.append({
            "key":          _s(t.get("key") or t.get("type"), "debt"),
            "type":         _s(t.get("type"), "Term Loan"),
            "name":         _s(t.get("name") or t.get("type"), "Debt Tranche"),
            "amount":       amt,
            "currency":     _s(t.get("currency"), "USD"),
            "rate":         _f(t.get("cash_rate") or t.get("rate"), 7.0),
            "base_rate":    _s(t.get("base_rate"), "SOFR"),
            "margin":       _f(t.get("margin"), 3.0),
            "pik_rate":     _f(t.get("pik_rate"), 0),
            "tenor":        _f(t.get("tenor_years") or t.get("tenor"), 5),
            "amortization": _s(t.get("amortization"), "linear"),
            "frequency":    _s(t.get("payment_frequency") or t.get("frequency"), "quarterly"),
            "drawn_pct":    _f(t.get("drawn_pct"), 1.0),
            "oid":          _f(t.get("oid"), 0),
            "upfront_fee":  _f(t.get("upfront_fee"), 0),
            "floor":        _f(t.get("floor"), 0),
            "pik_toggle":   bool(t.get("pik_toggle", False)),
            "grace_months": _i(t.get("grace_months"), 0),
        })
    total = sum(_f(t.get("amount")) for t in tranches)
    avg_r = (sum(_f(t.get("rate", 7)) * _f(t.get("amount")) for t in tranches) / total if total > 0 else 7.0)
    return {
        "tranches":      tranches,
        "total_debt":    total,
        "interest_rate": avg_r / 100 if avg_r > 1 else avg_r,
        "cash_sweep":    d.get("cash_sweep", False),
        "sweep_pct":     _f(d.get("sweep_pct"), 0.5),
        "covenant_leverage": _f(d.get("covenant_leverage"), 6.0),
        "covenant_icr":      _f(d.get("covenant_icr"), 2.0),
    }

class LoginRequest(BaseModel):
    license_key: str

class GenerateRequest(BaseModel):
    license_key: str
    config: dict

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "5.0", "suite": "Investment Banking"}

@app.post("/api/auth/login")
def login(req: LoginRequest):
    info = _check_license(req.license_key)
    return {"success": True, "user": info["user"], "license_key": req.license_key.strip().upper()}

@app.post("/api/generate")
def generate(req: GenerateRequest):
    _check_license(req.license_key)
    try:
        from build import build_model
        flat    = _map_config(req.config)
        file_id = str(uuid.uuid4())
        out     = str(OUTPUTS_DIR / f"bp_{file_id}.xlsx")
        build_model(flat, out)
        company = flat.get("company_name", "BP").replace(" ", "_")[:30]
        return {"success": True, "file_id": file_id, "filename": f"{company}_BP.xlsx"}
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=str(e) + "\n" + traceback.format_exc()[-800:])

@app.get("/api/download/{file_id}")
def download(file_id: str):
    path = OUTPUTS_DIR / f"bp_{file_id}.xlsx"
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found or expired")
    return FileResponse(str(path),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="BP_Generator.xlsx")

@app.post("/api/import")
async def import_financials(file: UploadFile = File(...), license_key: str = Form(...)):
    _check_license(license_key)
    ext = (file.filename or "").rsplit(".", 1)[-1].lower()
    if ext not in {"xlsx","xls","xlsm","csv","pdf"}:
        raise HTTPException(status_code=400, detail=f"Unsupported: .{ext}")
    file_bytes = await file.read()
    if len(file_bytes) > 50*1024*1024:
        raise HTTPException(status_code=400, detail="File too large (max 50MB)")
    try:
        from extractor_llm import extract_financials_llm
        result = await extract_financials_llm(file_bytes, file.filename)
        try:
            from financial_normalizer import normalise_from_extractor_payload
            result["normalised_model"] = normalise_from_extractor_payload(result)
        except Exception:
            pass
        return JSONResponse(content=result)
    except Exception as e1:
        try:
            from extractor import extract_financials, map_to_bp_actuals, build_projections_from_actuals
            import tempfile as tf2
            with tf2.NamedTemporaryFile(suffix=f".{ext}", delete=False) as tmp:
                tmp.write(file_bytes)
                tmp_path = tmp.name
            raw    = extract_financials(tmp_path)
            mapped = map_to_bp_actuals(raw)
            proj   = build_projections_from_actuals(mapped)
            Path(tmp_path).unlink(missing_ok=True)
            resp={"success": True, "fallback": True,
                "data_quality": proj["data_quality"], "hist_years": proj["hist_years"],
                "last_actuals": proj["last_actuals"], "suggestions": proj["proj_assumptions"]}
            try:
                from financial_normalizer import normalise_from_extractor_payload
                resp["normalised_model"] = normalise_from_extractor_payload(resp)
            except Exception:
                pass
            return JSONResponse(content=resp)
        except Exception as e2:
            raise HTTPException(status_code=500, detail=str(e2))

class DeckGenerateRequest(BaseModel):
    license_key: str
    config: dict = {}
    extracted_payload: dict = {}

@app.post("/api/generate_deck")
def generate_deck(req: DeckGenerateRequest):
    _check_license(req.license_key)
    try:
        from deck_generator import generate_im_deck_from_payload, generate_im_deck_from_config
        file_id = str(uuid.uuid4())
        out = str(DECKS_DIR / f"im_{file_id}.pptx")
        template_path = BASE_DIR / "templates" / "kpmg" / "Book Schemas Janvier 2023.pptx"
        template = str(template_path) if template_path.exists() else None
        if req.extracted_payload:
            meta = generate_im_deck_from_payload(req.extracted_payload, out, template_path=template)
        else:
            meta = generate_im_deck_from_config(req.config, out, template_path=template)
        company = (meta.get("company_name") or "Target").replace(" ", "_")[:30]
        return {"success": True, "file_id": file_id, "filename": f"{company}_IM_deck.pptx", "meta": meta}
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=str(e) + "\n" + traceback.format_exc()[-1200:])

@app.get("/api/download_deck/{file_id}")
def download_deck(file_id: str):
    path = DECKS_DIR / f"im_{file_id}.pptx"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Deck not found or expired")
    return FileResponse(str(path),
        media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        filename="Information_Memorandum.pptx")

@app.get("/")
def root():
    return FileResponse(str(INDEX)) if INDEX.exists() else HTMLResponse("<h2>BP Generator</h2>")

@app.get("/{full_path:path}")
def catch_all(full_path: str):
    asset = BASE_DIR / full_path
    if asset.exists() and asset.is_file() and not asset.suffix == ".py":
        return FileResponse(str(asset))
    return FileResponse(str(INDEX)) if INDEX.exists() else HTTPException(status_code=404)
