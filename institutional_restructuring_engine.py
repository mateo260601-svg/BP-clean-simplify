from typing import Dict, Any
import pandas as pd
from institutional_bp_engine import build_projection, clean_intake

def build_restructuring_pack(intake: Dict[str, Any], output_path: str) -> str:
    x = clean_intake(intake)
    projection = build_projection(x)["projection"]

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        wb = writer.book
        title = wb.add_format({"bold": True, "font_size": 18, "font_color": "#061A3A"})
        header = wb.add_format({"bold": True, "font_color": "white", "bg_color": "#061A3A", "border": 1})
        money = wb.add_format({"num_format": '#,##0.0', "border": 1})
        multiple = wb.add_format({"num_format": '0.0x', "border": 1})

        liquidity = []
        opening_cash = x["cash"]
        for row in projection:
            liquidity.append({
                "Year": row["year"],
                "Opening Cash": opening_cash,
                "EBITDA": row["ebitda"],
                "Interest": row["interest"],
                "Tax": row["tax"],
                "Capex": row["capex"],
                "FCF": row["fcf"],
                "Closing Cash": row["cash"],
                "Debt": row["debt"],
                "Net Debt": row["net_debt"],
                "Net Debt / EBITDA": row["net_debt_ebitda"],
            })
            opening_cash = row["cash"]
        sheets = {
            "Liquidity": pd.DataFrame(liquidity),
            "Debt Stack": pd.DataFrame([
                ["Senior Debt", x["debt"], x["interest_rate"], "Cash sweep"],
                ["RCF", "", "", "To be added"],
                ["Leases", "", "", "To be added"],
                ["Shareholder loans", "", "", "To be added"],
            ], columns=["Instrument", "Amount", "Rate", "Terms"]),
            "Covenants": pd.DataFrame([
                ["Net Debt / EBITDA", "< 4.5x", "", "Test quarterly"],
                ["ICR", "> 2.0x", "", "Test quarterly"],
                ["Minimum liquidity", "> 10m", "", "Weekly cash report"],
            ], columns=["Covenant", "Threshold", "Actual", "Comment"]),
            "Options Analysis": pd.DataFrame([
                ["Equity injection", "Improves liquidity", "Dilution"],
                ["Debt amend & extend", "Time to execute plan", "Lender approval"],
                ["Asset sale", "Deleveraging", "Execution risk"],
                ["Cost reduction", "Margin improvement", "Operational disruption"],
                ["Working capital release", "Cash generation", "Customer / supplier impact"],
            ], columns=["Option", "Benefit", "Risk"])
        }

        for sheet, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet, index=False, startrow=3)
            ws = writer.sheets[sheet]
            ws.write(0, 0, sheet, title)
            for c, col in enumerate(df.columns):
                ws.write(3, c, col, header)
                ws.set_column(c, c, 22)
            ws.freeze_panes(4, 0)
            ws.hide_gridlines(2)

    return output_path
