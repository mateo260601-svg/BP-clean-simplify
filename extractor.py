"""
Fallback financial extractor for BP Generator.
Supports xlsx/xlsm/csv/pdf text extraction without LLM.
Returns a normalized legacy structure used by /api/import fallback.
"""
import csv, io, re
from pathlib import Path
from typing import Dict, List, Tuple, Any

LABELS = {
    "revenue": ["revenue", "sales", "turnover", "chiffre d", "ca ", "produits d'exploitation", "net sales"],
    "ebitda": ["ebitda", "ebe", "operating profit before", "résultat d'exploitation avant", "earnings before interest"],
    "net_income": ["net income", "profit for the year", "résultat net", "benefice net", "bénéfice net"],
    "gross_debt": ["financial debt", "borrowings", "loans", "dette financière", "emprunts", "gross debt"],
    "cash": ["cash", "cash and cash equivalents", "trésorerie", "banque", "bank balances"],
    "trade_receivables": ["trade receivables", "accounts receivable", "créances clients", "clients et comptes rattachés"],
    "inventories": ["inventories", "stock", "stocks", "inventory"],
    "trade_payables": ["trade payables", "accounts payable", "dettes fournisseurs", "fournisseurs"],
}
YEAR_RE = re.compile(r"\b(20\d{2}|19\d{2})\b")
NUM_RE = re.compile(r"\(?-?\d[\d\s,.'’]*\)?")

def _num(v: Any):
    if v is None: return None
    if isinstance(v, (int, float)): return float(v)
    s = str(v).strip().replace("\u00a0", " ").replace("’", "'")
    if not s or not re.search(r"\d", s): return None
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("() ").replace(" ", "").replace("'", "")
    if "," in s and "." in s:
        s = s.replace(",", "") if s.rfind(".") > s.rfind(",") else s.replace(".", "").replace(",", ".")
    elif "," in s:
        parts = s.split(",")
        s = s.replace(",", ".") if len(parts[-1]) in (1,2) else s.replace(",", "")
    try:
        n = float(s)
        return -n if neg else n
    except Exception:
        return None

def _scale_to_k(n: float) -> float:
    # Heuristic: audited accounts often in actual currency; convert huge actuals to k.
    if abs(n) > 10_000_000: return n / 1000
    return n

def _read_xlsx(path: str) -> List[List[Any]]:
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    rows = []
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            vals = list(row)
            if any(v not in (None, "") for v in vals): rows.append(vals)
    return rows

def _read_csv(path: str) -> List[List[str]]:
    raw = Path(path).read_bytes()
    text = raw.decode("utf-8-sig", errors="replace")
    sample = text[:2048]
    dialect = csv.Sniffer().sniff(sample, delimiters=",;\t") if sample else csv.excel
    return [r for r in csv.reader(io.StringIO(text), dialect) if any(c.strip() for c in r)]

def _read_pdf(path: str) -> List[List[str]]:
    rows = []
    try:
        import pdfplumber
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages[:30]:
                for table in page.extract_tables() or []:
                    for r in table or []: rows.append([c or "" for c in r])
                txt = page.extract_text() or ""
                for line in txt.splitlines(): rows.append(re.split(r"\s{2,}|\t", line.strip()))
    except Exception:
        pass
    return rows

def _load_rows(path: str) -> List[List[Any]]:
    ext = Path(path).suffix.lower()
    if ext in [".xlsx", ".xlsm"]: return _read_xlsx(path)
    if ext == ".csv": return _read_csv(path)
    if ext == ".pdf": return _read_pdf(path)
    if ext == ".xls":
        try:
            import pandas as pd
            frames = pd.read_excel(path, sheet_name=None, header=None)
            return [list(r) for df in frames.values() for r in df.fillna("").values.tolist()]
        except Exception:
            return []
    return []

def _detect_years(rows: List[List[Any]]) -> List[str]:
    years = []
    for row in rows[:80]:
        for c in row:
            m = YEAR_RE.search(str(c))
            if m and m.group(1) not in years: years.append(m.group(1))
    return sorted(years)[-5:]

def _row_label(row):
    return " ".join(str(c).lower() for c in row[:4] if c not in (None, ""))

def extract_financials(path: str) -> Dict[str, Dict[str, float]]:
    rows = _load_rows(path)
    years = _detect_years(rows)
    data = {k: {} for k in LABELS}
    if not rows or not years: return {"periods": years, "metrics": data}

    for row in rows:
        label = _row_label(row)
        if not label: continue
        metric = None
        for k, aliases in LABELS.items():
            if any(a in label for a in aliases):
                metric = k; break
        if not metric: continue
        # Map by columns containing year headers if possible; otherwise use right-most numbers.
        nums = [_num(c) for c in row]
        vals = [n for n in nums if n is not None]
        if not vals: continue
        for y in years:
            idx = next((i for i,c in enumerate(row) if y in str(c)), None)
            if idx is not None:
                for j in range(idx+1, min(idx+4, len(row))):
                    n = _num(row[j])
                    if n is not None:
                        data[metric][y] = round(_scale_to_k(n), 1); break
        if not data[metric]:
            take = vals[-len(years):]
            for y, n in zip(years[-len(take):], take): data[metric][y] = round(_scale_to_k(n), 1)
    return {"periods": years, "metrics": data}

def map_to_bp_actuals(raw: Dict) -> Dict:
    return raw

def build_projections_from_actuals(mapped: Dict) -> Dict:
    metrics = mapped.get("metrics", {})
    years = mapped.get("periods", [])
    last = years[-1] if years else None
    def v(k):
        if not last: return 0
        return abs(float(metrics.get(k, {}).get(last, 0) or 0))
    last_actuals = {
        "revenue": v("revenue"), "ebitda": v("ebitda"), "net_income": v("net_income"),
        "gross_debt": v("gross_debt"), "cash": v("cash"),
    }
    rev = [float(metrics.get("revenue", {}).get(y, 0) or 0) for y in years]
    growths = [(rev[i]-rev[i-1])/rev[i-1] for i in range(1,len(rev)) if rev[i-1] > 0]
    ebitda = [float(metrics.get("ebitda", {}).get(y, 0) or 0) for y in years]
    margins = [e/r for e,r in zip(ebitda, rev) if r > 0]
    sugg = {
        "revenue": [last_actuals["revenue"]] if last_actuals["revenue"] else [],
        "revenue_growth": [sum(growths)/len(growths)] if growths else [],
        "ebitda_margin": [sum(margins)/len(margins)] if margins else [],
    }
    found = sum(1 for x in last_actuals.values() if x)
    score = round(found/5*100)
    label = "Excellent" if score >= 80 else "Good" if score >= 60 else "Partial" if score >= 40 else "Low"
    return {"hist_years": years, "last_actuals": last_actuals, "proj_assumptions": sugg, "data_quality": {"score": score, "label": label}}
