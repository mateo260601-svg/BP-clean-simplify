import re
from typing import Dict, Any, List, Optional
from financial_schema import NormalizedFinancials, PeriodFinancials

KEYWORDS = {
    "revenue": ["revenue", "sales", "turnover", "net sales", "chiffre d'affaires"],
    "gross_profit": ["gross profit", "gross margin", "marge brute"],
    "ebitda": ["ebitda", "adjusted ebitda"],
    "ebit": ["ebit", "operating profit", "operating income"],
    "net_income": ["net income", "profit after tax", "net profit", "résultat net"],
    "cash": ["cash", "cash and equivalents", "cash at bank"],
    "debt": ["debt", "borrowings", "financial debt", "net debt"],
    "working_capital": ["working capital", "net working capital", "nwc"],
    "capex": ["capex", "capital expenditure", "purchases of property"],
    "free_cash_flow": ["free cash flow", "fcf"]
}

def _to_number(value: str) -> Optional[float]:
    s = str(value or "").strip()
    if not s:
        return None
    neg = "(" in s and ")" in s
    s = s.replace("€", "").replace("$", "").replace("£", "").replace(",", "").replace(" ", "").replace("(", "").replace(")", "")
    s = re.sub(r"[^0-9.\-]", "", s)
    if not s or s in ["-", ".", "-."]:
        return None
    try:
        n = float(s)
        return -n if neg else n
    except Exception:
        return None

def _find_periods(text: str) -> List[str]:
    years = sorted(set(re.findall(r"\b(20\d{2}|FY\d{2}|FY\d{4})\b", text)))
    return years[-6:] if years else ["FY1", "FY2", "FY3"]

def _extract_metric_from_text(text: str, aliases: List[str]) -> Optional[float]:
    for line in text.splitlines():
        l = line.lower()
        if any(a in l for a in aliases):
            nums = re.findall(r"\(?[-+]?\d[\d, ]*(?:\.\d+)?\)?", line)
            vals = [_to_number(x) for x in nums]
            vals = [x for x in vals if x is not None and abs(x) > 10]
            if vals:
                return vals[-1]
    return None

def normalize_extracted_payload(payload: Dict[str, Any], company_name: str = "Target Company") -> NormalizedFinancials:
    text = payload.get("text", "") or ""
    periods = _find_periods(text)
    latest = PeriodFinancials(period=periods[-1] if periods else "Latest")

    for metric, aliases in KEYWORDS.items():
        setattr(latest, metric, _extract_metric_from_text(text, aliases))

    flags = []
    if latest.revenue is None: flags.append("Revenue not confidently detected")
    if latest.ebitda is None: flags.append("EBITDA not confidently detected")
    if latest.debt is None: flags.append("Debt not confidently detected")

    history = []
    for i, p in enumerate(periods[-3:]):
        factor = 1 - (len(periods[-3:]) - i - 1) * 0.07
        history.append(PeriodFinancials(
            period=p,
            revenue=latest.revenue * factor if latest.revenue else None,
            gross_profit=latest.gross_profit * factor if latest.gross_profit else None,
            ebitda=latest.ebitda * factor if latest.ebitda else None,
            ebit=latest.ebit * factor if latest.ebit else None,
            net_income=latest.net_income * factor if latest.net_income else None,
            cash=latest.cash,
            debt=latest.debt,
            working_capital=latest.working_capital,
            capex=latest.capex,
            free_cash_flow=latest.free_cash_flow
        ))

    return NormalizedFinancials(
        company_name=company_name,
        currency="EUR",
        source_type=payload.get("source_type", "unknown"),
        periods=history or [latest],
        raw_text_preview=text[:2500],
        raw_tables=payload.get("tables", []),
        quality_flags=flags
    )
