import re
from typing import Dict, Any, List


CORE_METRICS = [
    "revenue", "gross_profit", "ebitda", "ebit", "net_income",
    "cash", "debt", "net_debt", "capex", "receivables", "inventory",
    "payables", "working_capital", "depreciation", "interest_expense", "tax"
]


def _num(v, default=None):
    try:
        if v in [None, ""]:
            return default
        if isinstance(v, str):
            v = v.replace(" ", "").replace(",", ".").replace("%", "")
        return float(v)
    except Exception:
        return default


def _period_sort_key(period: str):
    p = str(period or "").upper().replace(" ", "")
    m = re.search(r"20\d{2}", p)
    year = int(m.group(0)) if m else 0

    q = 0
    qm = re.search(r"Q([1-4])", p)
    if qm:
        q = int(qm.group(1))

    month_map = {
        "JAN": 1, "FEB": 2, "MAR": 3, "APR": 4, "MAY": 5, "JUN": 6,
        "JUL": 7, "AUG": 8, "SEP": 9, "SEPT": 9, "OCT": 10, "NOV": 11, "DEC": 12,
        "JANVIER": 1, "FEVRIER": 2, "FÉVRIER": 2, "MARS": 3, "AVRIL": 4,
        "MAI": 5, "JUIN": 6, "JUILLET": 7, "AOUT": 8, "AOÛT": 8,
        "SEPTEMBRE": 9, "OCTOBRE": 10, "NOVEMBRE": 11, "DECEMBRE": 12, "DÉCEMBRE": 12,
    }

    month = 12 if year else 0
    for token, val in month_map.items():
        if token in p:
            month = val
            break

    if q:
        month = q * 3

    return (year, month, p)


def normalize_historical_accounts(extraction_payloads: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Consolidates all uploaded historical account extractions into a clean historical database.
    Supports:
    - deterministic extraction payloads
    - Claude-enhanced payloads
    - raw metric evidence fallback
    """
    by_period: Dict[str, Dict[str, Any]] = {}
    evidence: List[Dict[str, Any]] = []

    for payload in extraction_payloads or []:
        file_name = payload.get("file_name", "uploaded_file")

        # 1. Claude enhanced result
        ai_result = (payload.get("ai") or {}).get("result") or payload.get("normalized_ai")
        if isinstance(ai_result, dict) and ai_result.get("periods"):
            for row in ai_result.get("periods") or []:
                period = str(row.get("period") or "UNKNOWN").upper().replace(" ", "")
                if period not in by_period:
                    by_period[period] = {"period": period}

                for metric in CORE_METRICS:
                    if row.get(metric) is not None:
                        by_period[period][metric] = _num(row.get(metric))
                        evidence.append({
                            "file": file_name,
                            "period": period,
                            "metric": metric,
                            "value": row.get(metric),
                            "source": "claude",
                            "confidence": ai_result.get("confidence", 0.75),
                            "raw_label": metric,
                        })

        # 2. Deterministic normalized payload
        normalized = payload.get("normalized") or {}
        for row in normalized.get("periods") or []:
            period = str(row.get("period") or "UNKNOWN").upper().replace(" ", "")
            if period not in by_period:
                by_period[period] = {"period": period}

            for metric in CORE_METRICS:
                if row.get(metric) is not None and by_period[period].get(metric) is None:
                    by_period[period][metric] = _num(row.get(metric))
                    evidence.append({
                        "file": file_name,
                        "period": period,
                        "metric": metric,
                        "value": row.get(metric),
                        "source": "deterministic",
                        "confidence": normalized.get("confidence", 0.55),
                        "raw_label": metric,
                    })

        # 3. Raw metric evidence fallback
        for m in payload.get("metrics") or []:
            period = str(m.get("period") or "UNKNOWN").upper().replace(" ", "")
            metric = m.get("metric")
            if metric not in CORE_METRICS:
                continue

            value = _num(m.get("value"))
            if value is None:
                continue

            if period not in by_period:
                by_period[period] = {"period": period}

            if by_period[period].get(metric) is None:
                by_period[period][metric] = value

            evidence.append({
                "file": file_name,
                "period": period,
                "metric": metric,
                "value": value,
                "source": m.get("source", "metric_evidence"),
                "confidence": m.get("confidence", 0.45),
                "raw_label": m.get("raw_label", ""),
            })

    periods = sorted(by_period.values(), key=lambda x: _period_sort_key(x.get("period")))

    for row in periods:
        revenue = _num(row.get("revenue"))
        gross_profit = _num(row.get("gross_profit"))
        ebitda = _num(row.get("ebitda"))
        cash = _num(row.get("cash"))
        debt = _num(row.get("debt"))
        receivables = _num(row.get("receivables"))
        inventory = _num(row.get("inventory"))
        payables = _num(row.get("payables"))

        if cash is not None and debt is not None:
            row["net_debt"] = debt - cash

        if receivables is not None and inventory is not None and payables is not None:
            row["working_capital"] = receivables + inventory - payables

        if revenue:
            if gross_profit is not None:
                row["gross_margin"] = gross_profit / revenue
            if ebitda is not None:
                row["ebitda_margin"] = ebitda / revenue

    latest = periods[-1] if periods else {}
    first = periods[0] if periods else {}

    cagr = None
    if first.get("revenue") and latest.get("revenue") and len(periods) > 1:
        years = max(1, len(periods) - 1)
        cagr = (latest["revenue"] / first["revenue"]) ** (1 / years) - 1

    assumptions = {
        "revenue": latest.get("revenue", 202000),
        "revenue_growth": cagr if cagr is not None else 0.073,
        "gross_margin": latest.get("gross_margin", 0.391),
        "ebitda_margin": latest.get("ebitda_margin", 0.229),
        "cash": latest.get("cash", 18700),
        "debt": latest.get("debt", 201000),
        "dso": 55,
        "dio": 40,
        "dpo": 55,
    }

    completeness = {}
    for metric in CORE_METRICS:
        completeness[metric] = sum(1 for p in periods if p.get(metric) is not None)

    warnings = []
    for required in ["revenue", "ebitda", "cash", "debt"]:
        if completeness.get(required, 0) == 0:
            warnings.append(f"Missing historical {required}")

    return {
        "periods": periods,
        "latest": latest,
        "assumptions": assumptions,
        "evidence": evidence,
        "completeness": completeness,
        "warnings": warnings,
    }


def merge_historical_into_intake(intake: Dict[str, Any], historical: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merges normalized historical assumptions into the SaaS/BP intake.
    """
    out = dict(intake or {})
    assumptions = historical.get("assumptions") or {}

    for k, v in assumptions.items():
        if v is not None:
            out[k] = v

    out["historical_periods_count"] = len(historical.get("periods") or [])
    out["historical_warnings"] = historical.get("warnings") or []

    return out
