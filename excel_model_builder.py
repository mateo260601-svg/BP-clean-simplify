import pandas as pd
from financial_schema import NormalizedFinancials

def build_excel_model(financials: NormalizedFinancials, output_path: str) -> str:
    rows = []
    for p in financials.periods:
        rows.append({
            "Period": p.period,
            "Revenue": p.revenue,
            "Gross Profit": p.gross_profit,
            "EBITDA": p.ebitda,
            "EBIT": p.ebit,
            "Net Income": p.net_income,
            "Cash": p.cash,
            "Debt": p.debt,
            "Working Capital": p.working_capital,
            "Capex": p.capex,
            "Free Cash Flow": p.free_cash_flow,
        })
    df = pd.DataFrame(rows)

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        wb = writer.book
        title = wb.add_format({"bold": True, "font_size": 16, "font_color": "#0B1533"})
        header = wb.add_format({"bold": True, "font_color": "white", "bg_color": "#061A3A", "border": 1, "align": "center"})
        money = wb.add_format({"num_format": '#,##0.0', "border": 1})
        pct = wb.add_format({"num_format": "0.0%", "border": 1})

        summary = pd.DataFrame([
            ["Company", financials.company_name],
            ["Currency", financials.currency],
            ["Source", financials.source_type],
            ["Quality Flags", "; ".join(financials.quality_flags) if financials.quality_flags else "No major flags"]
        ], columns=["Field", "Value"])
        summary.to_excel(writer, sheet_name="Summary", index=False, startrow=2)
        ws = writer.sheets["Summary"]
        ws.write("A1", "Investment Banking Model Summary", title)
        ws.set_column("A:A", 24); ws.set_column("B:B", 80)
        for c, h in enumerate(summary.columns): ws.write(2, c, h, header)

        df.to_excel(writer, sheet_name="Financials", index=False, startrow=2)
        ws = writer.sheets["Financials"]
        ws.write("A1", "Historical Financials", title)
        ws.freeze_panes(3, 1)
        ws.set_column(0, len(df.columns), 18)
        for c, h in enumerate(df.columns): ws.write(2, c, h, header)
        for r in range(3, 3 + len(df)):
            for c in range(1, len(df.columns)):
                ws.write(r, c, df.iloc[r-3, c] if pd.notna(df.iloc[r-3, c]) else "", money)

        kpi_rows = []
        for p in financials.periods:
            revenue = p.revenue or 0
            ebitda = p.ebitda or 0
            debt = p.debt or 0
            cash = p.cash or 0
            kpi_rows.append({
                "Period": p.period,
                "EBITDA Margin": ebitda / revenue if revenue else "",
                "Net Debt": debt - cash if debt or cash else "",
                "Net Debt / EBITDA": (debt - cash) / ebitda if ebitda else ""
            })
        kpis = pd.DataFrame(kpi_rows)
        kpis.to_excel(writer, sheet_name="KPIs", index=False, startrow=2)
        ws = writer.sheets["KPIs"]
        ws.write("A1", "Key Performance Indicators", title)
        ws.set_column(0, len(kpis.columns), 22)
        for c, h in enumerate(kpis.columns): ws.write(2, c, h, header)

        qoe = pd.DataFrame([
            ["Reported EBITDA", ""],
            ["One-off costs", ""],
            ["Non-recurring income", ""],
            ["Run-rate adjustments", ""],
            ["Adjusted EBITDA", ""],
        ], columns=["Adjustment", "Amount"])
        qoe.to_excel(writer, sheet_name="QoE Adjustments", index=False, startrow=2)
        writer.sheets["QoE Adjustments"].write("A1", "Quality of Earnings Adjustments", title)

        raw = pd.DataFrame([[financials.raw_text_preview or ""]], columns=["Raw Text Preview"])
        raw.to_excel(writer, sheet_name="Raw Data", index=False)
    return output_path
