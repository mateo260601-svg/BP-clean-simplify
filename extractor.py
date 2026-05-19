from pathlib import Path
from typing import Dict, Any, List
import pdfplumber
import pandas as pd

def extract_pdf_text(path: str) -> str:
    text = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                text.append(page_text)
    return "\n".join(text)

def extract_pdf_tables(path: str) -> List[Dict[str, Any]]:
    tables = []
    with pdfplumber.open(path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            for table in page.extract_tables() or []:
                if table and len(table) > 1:
                    tables.append({"page": page_number, "headers": table[0], "rows": table[1:]})
    return tables

def extract_excel_sheets(path: str) -> Dict[str, Any]:
    xls = pd.ExcelFile(path)
    output = {}
    for sheet in xls.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet, header=None)
        df = df.dropna(how="all").dropna(axis=1, how="all")
        output[sheet] = df.astype(str).fillna("").values.tolist()
    return output

def extract_document(path: str) -> Dict[str, Any]:
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        return {"source_type": "pdf", "text": extract_pdf_text(path), "tables": extract_pdf_tables(path)}
    if suffix in [".xlsx", ".xls", ".xlsm", ".csv"]:
        if suffix == ".csv":
            df = pd.read_csv(path, header=None)
            return {"source_type": "csv", "sheets": {"CSV": df.astype(str).fillna("").values.tolist()}, "text": df.to_csv(index=False)}
        sheets = extract_excel_sheets(path)
        flat_text = "\n".join([f"## {name}\n{rows[:80]}" for name, rows in sheets.items()])
        return {"source_type": "excel", "sheets": sheets, "text": flat_text}
    raise ValueError(f"Unsupported file type: {suffix}")
