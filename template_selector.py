"""template_selector.py — deterministic IM slide selection rules."""
from __future__ import annotations
from typing import Dict, List

SLIDE_CATALOG = [
    {"id":"cover", "title":"Cover", "requires":[], "section":"Opening"},
    {"id":"disclaimer", "title":"Disclaimer", "requires":[], "section":"Opening"},
    {"id":"contents", "title":"Contents", "requires":[], "section":"Opening"},
    {"id":"executive_summary", "title":"Executive Summary", "requires_any":["revenue","ebitda","cash","debt"], "section":"Executive Summary"},
    {"id":"investment_highlights", "title":"Investment Highlights", "requires_any":["revenue","ebitda"], "section":"Executive Summary"},
    {"id":"financial_overview", "title":"Financial Overview", "requires":["revenue"], "section":"Financials"},
    {"id":"profitability", "title":"Profitability & Margin Profile", "requires_any":["gross_profit","ebitda","ebit","net_income"], "section":"Financials"},
    {"id":"cash_debt_liquidity", "title":"Cash, Debt & Liquidity", "requires_any":["cash","debt"], "section":"Financials"},
    {"id":"working_capital", "title":"Working Capital", "requires_any":["inventory","receivables","payables","working_capital"], "section":"Financials"},
    {"id":"value_creation", "title":"Value Creation Opportunity", "requires_any":["revenue","ebitda"], "section":"Investment Case"},
    {"id":"data_quality", "title":"Data Quality & Diligence Items", "requires":[], "section":"Appendix"},
    {"id":"process_next_steps", "title":"Process & Next Steps", "requires":[], "section":"Process"},
]

def _available(model: Dict) -> set:
    fin = model.get("financials", {}) or {}
    return {k for k,v in fin.items() if isinstance(v,dict) and any(x is not None for x in v.values())}

def select_slides(model: Dict) -> List[Dict]:
    available = _available(model); out=[]
    for s in SLIDE_CATALOG:
        req=set(s.get("requires",[])); req_any=set(s.get("requires_any",[]))
        ok = req.issubset(available) and (not req_any or bool(req_any & available))
        out.append({**s, "status":"included" if ok else "excluded", "missing":sorted(req - available), "available":sorted(available)})
    return out

def included_slides(model: Dict) -> List[Dict]:
    return [s for s in select_slides(model) if s["status"] == "included"]
