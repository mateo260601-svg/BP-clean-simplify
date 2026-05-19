"""
financial_normalizer.py — V2 institutional normalisation layer.
Converts heterogeneous PDF / Excel financial statements into a standard M&A data model.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Tuple
import math, re, json

CANONICAL = {
    "revenue": ["revenue", "turnover", "sales", "net sales", "chiffre d'affaires", "ca net", "produits d'exploitation"],
    "cogs": ["cost of sales", "cost of goods", "cogs", "raw materials", "matières", "achats consommés"],
    "gross_profit": ["gross profit", "gross margin", "marge brute"],
    "opex": ["operating expenses", "opex", "selling general", "sga", "sg&a", "admin expenses"],
    "ebitda": ["ebitda", "ebe", "earnings before interest", "adjusted ebitda"],
    "depreciation": ["depreciation", "amortisation", "amortization", "d&a", "dotations aux amortissements"],
    "ebit": ["ebit", "operating profit", "operating income", "résultat d'exploitation", "resultat d'exploitation"],
    "interest": ["interest", "finance cost", "financial expense", "charges financières"],
    "tax": ["tax", "income tax", "impôt", "impots"],
    "net_income": ["net income", "profit for the year", "net profit", "résultat net", "resultat net"],
    "cash": ["cash", "cash equivalents", "bank balances", "trésorerie", "tresorerie"],
    "debt": ["borrowings", "loans", "financial debt", "gross debt", "emprunts", "dette financière", "dette financiere"],
    "inventory": ["inventory", "inventories", "stock", "stocks"],
    "receivables": ["trade receivables", "accounts receivable", "créances clients", "creances clients"],
    "payables": ["trade payables", "accounts payable", "dettes fournisseurs"],
    "working_capital": ["working capital", "net working capital", "nwc", "bfr"],
    "capex": ["capex", "capital expenditure", "purchase of property", "investissements"],
    "cfo": ["cash flow from operations", "operating cash flow", "flux de trésorerie opérationnel"],
    "fcf": ["free cash flow", "fcf", "cash generation"],
}

@dataclass
class NormalisedFinancialModel:
    company_name: str = "Target Company"
    currency: str = "EUR"
    unit: str = "k"
    periods: List[str] = None
    financials: Dict[str, Dict[str, Optional[float]]] = None
    kpis: Dict[str, Dict[str, Optional[float]]] = None
    checks: Dict[str, Any] = None
    narrative: Dict[str, Any] = None
    source_quality: str = "medium"
    extraction_notes: List[str] = None

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["periods"] = d["periods"] or []
        d["financials"] = d["financials"] or {}
        d["kpis"] = d["kpis"] or {}
        d["checks"] = d["checks"] or {}
        d["narrative"] = d["narrative"] or {}
        d["extraction_notes"] = d["extraction_notes"] or []
        return d

def safe_float(x: Any) -> Optional[float]:
    if x is None or x == "": return None
    if isinstance(x, bool): return None
    if isinstance(x, (int, float)):
        try:
            f = float(x)
            return None if math.isnan(f) or math.isinf(f) else f
        except Exception: return None
    s = str(x).strip().replace("\u00a0", " ").replace("’", "'")
    if not re.search(r"\d", s): return None
    neg = (s.startswith("(") and s.endswith(")")) or s.startswith("-")
    s = s.strip("() ")
    multiplier = 1.0
    if re.search(r"\bm\b|million|m€|€m|usd m|gbp m", s, re.I): multiplier = 1000.0
    s = re.sub(r"[^0-9,\.\-]", "", s)
    if s.count(",") and s.count("."):
        s = s.replace(",", "") if s.rfind(".") > s.rfind(",") else s.replace(".", "").replace(",", ".")
    elif s.count(","):
        last = s.split(",")[-1]
        s = s.replace(",", ".") if len(last) in (1,2) else s.replace(",", "")
    try:
        v = abs(float(s)) * multiplier
        return -v if neg else v
    except Exception:
        return None

def norm_text(s: Any) -> str:
    s = str(s or "").lower()
    repl = {"é":"e","è":"e","ê":"e","ë":"e","à":"a","â":"a","ç":"c","ï":"i","î":"i","ô":"o","û":"u","ù":"u"}
    for a,b in repl.items(): s=s.replace(a,b)
    s = re.sub(r"[^a-z0-9% /&'\-]", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def detect_metric(label: Any) -> Optional[str]:
    s = norm_text(label)
    if not s: return None
    best = None
    for key, variants in CANONICAL.items():
        for v in variants:
            vv = norm_text(v)
            if vv and (vv == s or vv in s):
                best = key
                break
        if best: break
    return best

def detect_period(value: Any) -> Optional[str]:
    s = str(value or "")
    m = re.search(r"\b(FY|CY)?\s*(20\d{2}|19\d{2})\b", s, re.I)
    if m: return m.group(2)
    m = re.search(r"\b(\d{1,2})[\-/](\d{1,2})[\-/](20\d{2}|19\d{2})\b", s)
    if m: return m.group(3)
    return None

def _extract_financials_from_rows(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    out: Dict[str, Dict[str, float]] = {}
    for row in rows:
        if not isinstance(row, dict): continue
        label = row.get("metric") or row.get("line_item") or row.get("label") or row.get("name") or next(iter(row.values()), "")
        metric = detect_metric(label)
        if not metric: continue
        out.setdefault(metric, {})
        for k,v in row.items():
            p = detect_period(k)
            val = safe_float(v)
            if p and val is not None:
                out[metric][p] = val
    return out

def _coerce_financials(fin: Any) -> Dict[str, Dict[str, float]]:
    if isinstance(fin, list):
        return _extract_financials_from_rows(fin)
    if not isinstance(fin, dict):
        return {}
    out: Dict[str, Dict[str, float]] = {}
    for k,v in fin.items():
        metric = detect_metric(k) or norm_text(k).replace(" ", "_")
        if isinstance(v, dict):
            for pk,pv in v.items():
                p = detect_period(pk) or str(pk)
                val = safe_float(pv)
                if p and val is not None:
                    out.setdefault(metric, {})[p] = val
        elif isinstance(v, list):
            # list of period/value dicts
            for item in v:
                if isinstance(item, dict):
                    p = detect_period(item.get("period") or item.get("year"))
                    val = safe_float(item.get("value") or item.get("amount"))
                    if p and val is not None:
                        out.setdefault(metric, {})[p] = val
    return out

def compute_kpis(model: Dict[str, Any]) -> Dict[str, Dict[str, Optional[float]]]:
    fin = model.get("financials", {}) or {}; periods = [str(p) for p in model.get("periods", [])]
    kpis = {k:{} for k in ["revenue_growth","gross_margin","ebitda_margin","ebit_margin","net_margin","net_debt","net_debt_ebitda","nwc","nwc_pct_sales","fcf_conversion"]}
    prev_rev = None
    for p in periods:
        rev = safe_float((fin.get("revenue") or {}).get(p))
        gp = safe_float((fin.get("gross_profit") or {}).get(p))
        ebitda = safe_float((fin.get("ebitda") or {}).get(p))
        ebit = safe_float((fin.get("ebit") or {}).get(p))
        ni = safe_float((fin.get("net_income") or {}).get(p))
        cash = safe_float((fin.get("cash") or {}).get(p)) or 0
        debt = safe_float((fin.get("debt") or {}).get(p)) or 0
        inv = safe_float((fin.get("inventory") or {}).get(p)) or 0
        rec = safe_float((fin.get("receivables") or {}).get(p)) or 0
        pay = safe_float((fin.get("payables") or {}).get(p)) or 0
        fcf = safe_float((fin.get("fcf") or {}).get(p))
        nwc = inv + rec - pay
        kpis["revenue_growth"][p] = (rev/prev_rev - 1) if rev not in (None,0) and prev_rev not in (None,0) else None
        kpis["gross_margin"][p] = (gp/rev) if gp is not None and rev not in (None,0) else None
        kpis["ebitda_margin"][p] = (ebitda/rev) if ebitda is not None and rev not in (None,0) else None
        kpis["ebit_margin"][p] = (ebit/rev) if ebit is not None and rev not in (None,0) else None
        kpis["net_margin"][p] = (ni/rev) if ni is not None and rev not in (None,0) else None
        kpis["net_debt"][p] = debt - cash
        kpis["net_debt_ebitda"][p] = ((debt-cash)/ebitda) if ebitda not in (None,0) else None
        kpis["nwc"][p] = nwc if any([inv,rec,pay]) else None
        kpis["nwc_pct_sales"][p] = (nwc/rev) if rev not in (None,0) and any([inv,rec,pay]) else None
        kpis["fcf_conversion"][p] = (fcf/ebitda) if fcf is not None and ebitda not in (None,0) else None
        if rev not in (None,0): prev_rev = rev
    return kpis

def compute_checks(model: Dict[str, Any]) -> Dict[str, Any]:
    fin = model.get("financials", {}) or {}; periods = model.get("periods", []) or []
    available = sorted([k for k,v in fin.items() if isinstance(v, dict) and any(safe_float(x) is not None for x in v.values())])
    critical = ["revenue","ebitda","cash","debt"]
    missing = [x for x in critical if x not in available]
    score = 30 + min(len(periods), 5)*8 + sum(10 for x in critical if x in available)
    score = max(0, min(100, score))
    if score >= 80: quality = "Excellent"
    elif score >= 60: quality = "Good"
    elif score >= 40: quality = "Partial"
    else: quality = "Low"
    return {"quality_score": score, "quality_label": quality, "available_metrics": available, "missing_critical_metrics": missing, "period_count": len(periods), "has_pnl": "revenue" in available and ("ebitda" in available or "ebit" in available), "has_balance_sheet": any(x in available for x in ["cash","debt","inventory","receivables","payables"]), "has_cash_flow": any(x in available for x in ["cfo","fcf","capex"])}

def normalise_from_extractor_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    payload = payload if isinstance(payload, dict) else {}
    fin = payload.get("financials") or payload.get("data") or payload.get("last_actuals") or payload.get("raw") or {}
    financials = _coerce_financials(fin)
    # fallback: current import format uses last_actuals without periods
    if not financials and isinstance(payload.get("last_actuals"), dict):
        year = str((payload.get("hist_years") or ["Latest"])[-1])
        for k,v in payload["last_actuals"].items():
            metric = detect_metric(k) or {"gross_debt":"debt"}.get(k,k)
            val = safe_float(v)
            if val is not None: financials.setdefault(metric,{})[year]=val
    periods = payload.get("periods") or payload.get("hist_years") or sorted({str(p) for vals in financials.values() if isinstance(vals, dict) for p in vals.keys() if str(p)})
    periods = [str(p) for p in periods]
    model = NormalisedFinancialModel(
        company_name = payload.get("company_name") or payload.get("company") or payload.get("target") or "Target Company",
        currency = payload.get("currency") or payload.get("ccy") or "EUR",
        unit = payload.get("unit") or payload.get("units") or "k",
        periods = periods,
        financials = financials,
        narrative = payload.get("narrative") or payload.get("commentary") or {},
        source_quality = str(payload.get("source_quality") or payload.get("confidence") or "medium"),
        extraction_notes = payload.get("extraction_notes") or [],
    ).to_dict()
    model["kpis"] = compute_kpis(model)
    model["checks"] = compute_checks(model)
    return model

def model_from_bp_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Build a financial model from the existing wizard config when no upload payload is available."""
    c = config or {}; comp = c.get("company",{}) if isinstance(c.get("company"),dict) else {}
    rev = c.get("revenue",{}) if isinstance(c.get("revenue"),dict) else {}
    costs = c.get("costs",{}) if isinstance(c.get("costs"),dict) else {}
    debt = c.get("debt",{}) if isinstance(c.get("debt"),dict) else {}
    start = int(safe_float(rev.get("start_year")) or 2025); years = int(safe_float(rev.get("projection_years")) or 5)
    periods = [str(start+i) for i in range(years)]
    volume = safe_float(rev.get("base_volume")) or 0; price = safe_float(rev.get("price_per_unit")) or 0
    base_rev = safe_float(rev.get("base_revenue")) or (volume*price/1000 if volume and price else 50000)
    vg = (safe_float(rev.get("volume_growth")) or 0)/100 if (safe_float(rev.get("volume_growth")) or 0)>1 else (safe_float(rev.get("volume_growth")) or 0)
    pg = (safe_float(rev.get("price_growth")) or 0)/100 if (safe_float(rev.get("price_growth")) or 0)>1 else (safe_float(rev.get("price_growth")) or 0)
    gm = (safe_float(costs.get("gross_margin")) or 35)/100 if (safe_float(costs.get("gross_margin")) or 35)>1 else (safe_float(costs.get("gross_margin")) or .35)
    em = (safe_float(costs.get("ebitda_margin")) or 20)/100 if (safe_float(costs.get("ebitda_margin")) or 20)>1 else (safe_float(costs.get("ebitda_margin")) or .20)
    financials = {"revenue":{}, "gross_profit":{}, "ebitda":{}, "cash":{}, "debt":{}}
    total_debt = 0
    for t in debt.get("tranches",[]) if isinstance(debt,dict) else []:
        total_debt += safe_float(t.get("amount")) or 0
    for i,p in enumerate(periods):
        r = base_rev*((1+vg+pg)**i)
        financials["revenue"][p]=r; financials["gross_profit"][p]=r*gm; financials["ebitda"][p]=r*em
        financials["cash"][p]=safe_float(c.get("opening_cash")) or 0; financials["debt"][p]=total_debt
    return normalise_from_extractor_payload({"company_name": comp.get("name") or "Target Company", "currency": comp.get("currency") or "EUR", "periods": periods, "financials": financials, "source_quality":"wizard"})
