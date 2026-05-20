from typing import Dict, Any
import pandas as pd
from institutional_bp_engine import build_projection, clean_intake

def build_institutional_qoe(intake: Dict[str, Any], financials: Dict[str, Any], output_path: str) -> str:
    x = clean_intake(intake)
    projection = build_projection(x)["projection"]
    latest = projection[0] if projection else {}

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        wb = writer.book
        title = wb.add_format({"bold": True, "font_size": 18, "font_color": "#061A3A"})
        header = wb.add_format({"bold": True, "font_color": "white", "bg_color": "#061A3A", "border": 1})
        money = wb.add_format({"num_format": '#,##0.0', "border": 1})
        pct = wb.add_format({"num_format": '0.0%', "border": 1})

        sheets = {
            "QoE Summary": pd.DataFrame([
                ["Reported EBITDA", latest.get("ebitda", 0), "From BP / extracted accounts"],
                ["One-off costs", 0, "To be completed during QoE review"],
                ["Non-recurring income", 0, "To be completed during QoE review"],
                ["Run-rate savings", 0, "Management / diligence input"],
                ["Normalised EBITDA", latest.get("ebitda", 0), "Formula output"],
            ], columns=["Bridge Item", "Amount", "Comment"]),

            "Revenue Quality": pd.DataFrame([
                ["Contracted revenue %", x.get("contracted_revenue_pct", 0), "Validate contracts"],
                ["Customer concentration", "", "Top 10 customers required"],
                ["Recurring / repeat revenue", "", "Client input required"],
                ["Churn", x.get("churn", 0), "Validate cohort analysis"],
                ["Price vs volume split", "", "Management accounts required"],
            ], columns=["Check", "Value", "Diligence Action"]),

            "EBITDA Adjustments": pd.DataFrame([
                ["Management adjustments", "", "Open"],
                ["Owner costs", "", "Open"],
                ["Exceptional legal / advisory", "", "Open"],
                ["Run-rate headcount", "", "Open"],
                ["Bad debt / provisions", "", "Open"],
                ["FX / commodity normalization", "", "Open"],
            ], columns=["Adjustment", "Amount", "Status"]),

            "Working Capital": pd.DataFrame([
                ["DSO", x.get("dso"), "Receivables quality"],
                ["DIO", x.get("dio"), "Inventory aging"],
                ["DPO", x.get("dpo"), "Supplier terms"],
                ["NWC Peg", "", "Calculate from monthly data"],
                ["Seasonality", "", "Monthly detail required"],
            ], columns=["Metric", "Value", "Comment"]),

            "Debt-like Items": pd.DataFrame([
                ["Financial debt", x.get("debt"), "Input"],
                ["Leases", "", "Review IFRS16 / local GAAP"],
                ["Overdue payables", "", "Aging required"],
                ["Accrued taxes", "", "Tax review"],
                ["Customer advances", "", "Contract review"],
                ["Provisions", "", "Legal / HR review"],
            ], columns=["Item", "Amount", "Comment"]),

            "Open Questions": pd.DataFrame([
                ["Revenue recognition policy?", "Finance", "Open"],
                ["Top customer contracts and renewal terms?", "Commercial", "Open"],
                ["One-off costs in last 36 months?", "Finance", "Open"],
                ["Monthly working capital detail?", "Finance", "Open"],
                ["Debt-like items schedule?", "Finance", "Open"],
            ], columns=["Question", "Owner", "Status"])
        }

        for sheet, df in sheets.items():
            df.to_excel(writer, sheet_name=sheet, index=False, startrow=3)
            ws = writer.sheets[sheet]
            ws.write(0, 0, sheet, title)
            for c, col in enumerate(df.columns):
                ws.write(3, c, col, header)
                ws.set_column(c, c, 26)
            for r in range(4, 4 + len(df)):
                for c in range(len(df.columns)):
                    if c == 1:
                        ws.write(r, c, df.iloc[r-4, c], money if isinstance(df.iloc[r-4, c], (int, float)) else None)
            ws.freeze_panes(4, 0)
            ws.hide_gridlines(2)

    return output_path
