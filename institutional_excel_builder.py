from pathlib import Path
from typing import Dict, Any
import pandas as pd
import xlsxwriter
from institutional_bp_engine import build_projection, build_scenarios, clean_intake

NAVY = "#061A3A"
BLUE = "#0B5FFF"
LIGHT = "#F7FAFC"
GREEN = "#059669"
RED = "#DC2626"
GREY = "#64748B"

def _formats(wb):
    return {
        "title": wb.add_format({"bold": True, "font_size": 18, "font_color": NAVY}),
        "subtitle": wb.add_format({"font_size": 10, "font_color": GREY}),
        "header": wb.add_format({"bold": True, "font_color": "white", "bg_color": NAVY, "border": 1, "align": "center"}),
        "subheader": wb.add_format({"bold": True, "font_color": NAVY, "bg_color": "#EAF2FF", "border": 1}),
        "money": wb.add_format({"num_format": '#,##0.0', "border": 1}),
        "pct": wb.add_format({"num_format": '0.0%', "border": 1}),
        "multiple": wb.add_format({"num_format": '0.0x', "border": 1}),
        "text": wb.add_format({"border": 1}),
        "green": wb.add_format({"font_color": GREEN, "bold": True}),
        "red": wb.add_format({"font_color": RED, "bold": True}),
    }

def _write_df(writer, sheet, df, title, startrow=3):
    wb = writer.book
    fmt = _formats(wb)
    df.to_excel(writer, sheet_name=sheet, startrow=startrow, index=False)
    ws = writer.sheets[sheet]
    ws.write(0, 0, title, fmt["title"])
    ws.write(1, 0, "MG Advisory | Institutional Investment Banking Output", fmt["subtitle"])
    ws.freeze_panes(startrow + 1, 1)
    for c, col in enumerate(df.columns):
        ws.write(startrow, c, col, fmt["header"])
        ws.set_column(c, c, max(15, min(30, len(str(col)) + 4)))
    return ws

def build_institutional_bp_excel(intake: Dict[str, Any], output_path: str) -> str:
    x = clean_intake(intake)
    projection = build_projection(x)["projection"]
    scenarios = build_scenarios(x)

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        wb = writer.book
        fmt = _formats(wb)

        summary_rows = [
            ["Company", x["company_name"]],
            ["Sector", x["sector"]],
            ["Currency", x["currency"]],
            ["Deal type", x["deal_type"]],
            ["Forecast years", x["forecast_years"]],
            ["Revenue", x["revenue"]],
            ["Revenue growth", x["revenue_growth"]],
            ["EBITDA margin", x["ebitda_margin"]],
            ["Debt", x["debt"]],
            ["Cash", x["cash"]],
            ["Investment thesis", x.get("investment_thesis", "")],
            ["Value creation plan", x.get("value_creation_plan", "")],
            ["Key risks", x.get("key_risks", "")],
        ]
        summary = pd.DataFrame(summary_rows, columns=["Field", "Value"])
        _write_df(writer, "Executive Summary", summary, "Executive Summary")
        ws = writer.sheets["Executive Summary"]
        ws.set_column("A:A", 28)
        ws.set_column("B:B", 90)
        ws.conditional_format("B9:B10", {"type": "cell", "criteria": ">", "value": 0, "format": fmt["green"]})

        df = pd.DataFrame(projection)
        ordered = [
            "year", "revenue", "contracted_revenue", "new_business", "churn_impact",
            "gross_profit", "ebitda", "ebitda_margin", "depreciation", "ebit",
            "interest", "pbt", "tax", "net_income", "nwc", "capex", "fcf",
            "cash", "debt", "net_debt", "net_debt_ebitda", "fcf_conversion",
            "utilisation", "capacity_used", "fte", "revenue_per_fte"
        ]
        df = df[[c for c in ordered if c in df.columns]]
        ws = _write_df(writer, "Integrated Financials", df, "Integrated Financial Statements")
        for c, col in enumerate(df.columns):
            if "margin" in col or "conversion" in col or "utilisation" in col:
                ws.set_column(c, c, 16, fmt["pct"])
            elif col != "year":
                ws.set_column(c, c, 16, fmt["money"])

        pnl = df[["year", "revenue", "gross_profit", "ebitda", "depreciation", "ebit", "interest", "tax", "net_income"]].copy()
        _write_df(writer, "P&L", pnl, "Profit & Loss Statement")

        cf = df[["year", "ebitda", "tax", "nwc", "capex", "fcf", "cash", "debt", "net_debt"]].copy()
        _write_df(writer, "Cash Flow", cf, "Cash Flow & Debt Evolution")

        kpi_cols = ["year", "ebitda_margin", "net_debt_ebitda", "fcf_conversion", "utilisation", "revenue_per_fte"]
        kpis = df[[c for c in kpi_cols if c in df.columns]].copy()
        _write_df(writer, "KPIs", kpis, "KPIs & Credit Metrics")

        sens_rows = []
        for case, result in scenarios.items():
            last = result["projection"][-1]
            sens_rows.append({
                "Case": case,
                "Final Revenue": last["revenue"],
                "Final EBITDA": last["ebitda"],
                "Final EBITDA Margin": last["ebitda_margin"],
                "Final FCF": last["fcf"],
                "Net Debt / EBITDA": last["net_debt_ebitda"],
            })
        sensitivities = pd.DataFrame(sens_rows)
        _write_df(writer, "Scenarios", sensitivities, "Scenario Analysis")

        qoe = pd.DataFrame([
            ["Reported EBITDA", df.iloc[0]["ebitda"] if len(df) else 0, "From BP"],
            ["One-off costs", 0, "Client input required"],
            ["Non-recurring income", 0, "Client input required"],
            ["Run-rate adjustment", 0, "Client input required"],
            ["Adjusted EBITDA", "", "Formula / diligence output"],
        ], columns=["Adjustment", "Amount", "Comment"])
        _write_df(writer, "QoE Bridge", qoe, "QoE Bridge")

        debt = pd.DataFrame([
            ["Opening Debt", x["debt"]],
            ["Interest Rate", x["interest_rate"]],
            ["Cash Sweep", "50% of positive FCF"],
            ["Covenant 1", "Net Debt / EBITDA"],
            ["Covenant 2", "ICR / DSCR"],
        ], columns=["Debt Item", "Value"])
        _write_df(writer, "Debt & Covenants", debt, "Debt & Covenants")

        data_dict = pd.DataFrame([
            ["Revenue", "Top-line sales"],
            ["EBITDA", "Earnings before interest, taxes, depreciation and amortisation"],
            ["NWC", "Receivables + Inventory - Payables"],
            ["FCF", "EBITDA - Tax - Capex - NWC change"],
        ], columns=["Metric", "Definition"])
        _write_df(writer, "Data Dictionary", data_dict, "Data Dictionary")

        # Charts
        chart_sheet = wb.add_worksheet("Charts")
        writer.sheets["Charts"] = chart_sheet
        chart_sheet.write(0, 0, "Charts", fmt["title"])
        # Revenue / EBITDA chart from Integrated Financials
        chart = wb.add_chart({"type": "column"})
        n = len(df)
        chart.add_series({
            "name": "Revenue",
            "categories": ["Integrated Financials", 4, 0, 3+n, 0],
            "values": ["Integrated Financials", 4, 1, 3+n, 1],
        })
        chart.add_series({
            "name": "EBITDA",
            "categories": ["Integrated Financials", 4, 0, 3+n, 0],
            "values": ["Integrated Financials", 4, 6, 3+n, 6],
        })
        chart.set_title({"name": "Revenue and EBITDA"})
        chart.set_style(10)
        chart_sheet.insert_chart("A3", chart, {"x_scale": 1.5, "y_scale": 1.2})

        for sheet_name, ws in writer.sheets.items():
            try:
                ws.hide_gridlines(2)
            except Exception:
                pass

    return output_path
