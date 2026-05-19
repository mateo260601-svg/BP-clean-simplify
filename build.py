from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from styles import *

def build_model(config, output_path):
    wb = Workbook()
    wb.remove(wb.active)

    n = config.get("n_years", 5)
    start = config.get("start_year", 2025)
    company = config.get("company_name", "Company")
    ccy = config.get("currency", "USD")
    unit = f"{ccy}k"

    years = [{"fy": start + i, "is_actual": False} for i in range(n)]

    FIRST_COL = 5
    LABEL_COL = 2

    def col(i): return get_column_letter(FIRST_COL + i)

    def setup_sheet(wb, name, tab_color):
        ws = wb.create_sheet(name)
        ws.sheet_view.showGridLines = False
        ws.sheet_view.zoomScale = 90
        ws.sheet_properties.tabColor = tab_color
        ws.column_dimensions["A"].width = 2
        ws.column_dimensions["B"].width = 40
        ws.column_dimensions["C"].width = 8
        ws.column_dimensions["D"].width = 10
        for i in range(n):
            ws.column_dimensions[col(i)].width = 14
        return ws

    def title_row(ws, row, text):
        end = col(n - 1)
        ws.row_dimensions[row].height = 32
        cell = ws.cell(row=row, column=LABEL_COL, value=text)
        apply_style(cell, fill=fill_navy, font=font_title, alignment=align_center)
        for i in range(1, n + 3):
            c = ws.cell(row=row, column=LABEL_COL + i)
            apply_style(c, fill=fill_navy)

    def header_row(ws, row, years):
        ws.row_dimensions[row].height = 18
        for i, yr in enumerate(years):
            c = ws.cell(row=row, column=FIRST_COL + i, value=yr["fy"])
            apply_style(c, fill=fill_blue_header, font=font_header, alignment=align_center)

    def section(ws, row, label):
        ws.row_dimensions[row].height = 16
        c = ws.cell(row=row, column=LABEL_COL, value=label)
        apply_style(c, fill=fill_navy_light, font=font_header, alignment=align_left)
        for i in range(n):
            c2 = ws.cell(row=row, column=FIRST_COL + i)
            apply_style(c2, fill=fill_navy_light)

    def data_row(ws, row, label, values, bold=False, bg=None, fmt=FMT_INT, height=15):
        ws.row_dimensions[row].height = height
        c = ws.cell(row=row, column=LABEL_COL, value=label)
        f = font_bold if bold else font_normal
        b = bg or fill_white
        apply_style(c, font=f, fill=b, alignment=align_left)
        for i, v in enumerate(values):
            c2 = ws.cell(row=row, column=FIRST_COL + i, value=v)
            apply_style(c2, font=f, fill=b, alignment=align_right, number_format=fmt)

    # ── Revenue model ────────────────────────────────────────────────────────
    base_rev = config.get("base_revenue", 50000)
    rev_growth = config.get("revenue_growth", 0.05)
    gross_margin = config.get("gross_margin", 0.35)
    ebitda_margin = config.get("ebitda_margin", 0.20)
    tax_rate = config.get("tax_rate", 0.25)
    dso = config.get("dso", 45)
    dio = config.get("dio", 30)
    dpo = config.get("dpo", 40)

    revenues = [base_rev * ((1 + rev_growth) ** i) for i in range(n)]
    gross_profits = [r * gross_margin for r in revenues]
    ebitdas = [r * ebitda_margin for r in revenues]
    dep = config.get("capex", {}).get("opening_ppe", 85000) / 20
    depreciations = [dep] * n
    ebits = [e - dep for e in ebitdas]

    debt_cfg = config.get("debt", {})
    total_debt = debt_cfg.get("total_debt", 0)
    int_rate = debt_cfg.get("interest_rate", 0.065)
    interests = [total_debt * int_rate] * n
    pbts = [e - i for e, i in zip(ebits, interests)]
    taxes = [max(p * tax_rate, 0) for p in pbts]
    net_incomes = [p - t for p, t in zip(pbts, taxes)]

    # ── ASSUMPTIONS ─────────────────────────────────────────────────────────
    ws_a = setup_sheet(wb, "ASSUMPTIONS", "1F3D7A")
    title_row(ws_a, 1, f"{company}  —  Assumptions")
    header_row(ws_a, 3, years)
    section(ws_a, 4, "REVENUE DRIVERS")
    data_row(ws_a, 5, "Revenue growth %", [rev_growth] * n, fmt=FMT_PCT1)
    data_row(ws_a, 6, "Gross margin %", [gross_margin] * n, fmt=FMT_PCT1)
    data_row(ws_a, 7, "EBITDA margin %", [ebitda_margin] * n, fmt=FMT_PCT1)
    section(ws_a, 8, "NWC ASSUMPTIONS")
    data_row(ws_a, 9, "DSO (days)", [dso] * n, fmt=FMT_INT)
    data_row(ws_a, 10, "DIO (days)", [dio] * n, fmt=FMT_INT)
    data_row(ws_a, 11, "DPO (days)", [dpo] * n, fmt=FMT_INT)
    section(ws_a, 12, "TAX & MACRO")
    data_row(ws_a, 13, "Tax rate %", [tax_rate] * n, fmt=FMT_PCT1)
    data_row(ws_a, 14, "Inflation %", [config.get("inflation", 0.025)] * n, fmt=FMT_PCT1)

    # ── P&L ──────────────────────────────────────────────────────────────────
    ws_pl = setup_sheet(wb, "P&L", "0D1B3E")
    title_row(ws_pl, 1, f"{company}  —  Income Statement")
    header_row(ws_pl, 3, years)
    section(ws_pl, 4, "REVENUE")
    data_row(ws_pl, 5, f"Net Revenue ({unit})", revenues, bold=True, bg=fill_grey_light)
    data_row(ws_pl, 6, f"Gross Profit ({unit})", gross_profits, bg=fill_blue_light)
    data_row(ws_pl, 7, "Gross Margin %", [g/r for g, r in zip(gross_profits, revenues)], fmt=FMT_PCT1)
    section(ws_pl, 8, "EBITDA")
    data_row(ws_pl, 9, f"Adj. EBITDA ({unit})", ebitdas, bold=True, bg=fill_blue_light)
    data_row(ws_pl, 10, "EBITDA Margin %", [e/r for e, r in zip(ebitdas, revenues)], fmt=FMT_PCT1)
    section(ws_pl, 11, "EBIT")
    data_row(ws_pl, 12, f"D&A ({unit})", [-d for d in depreciations])
    data_row(ws_pl, 13, f"EBIT ({unit})", ebits, bold=True, bg=fill_blue_light)
    section(ws_pl, 14, "NET INCOME")
    data_row(ws_pl, 15, f"Net Interest ({unit})", [-i for i in interests])
    data_row(ws_pl, 16, f"PBT ({unit})", pbts)
    data_row(ws_pl, 17, f"Tax ({unit})", [-t for t in taxes])
    data_row(ws_pl, 18, f"Net Income ({unit})", net_incomes, bold=True, bg=fill_blue_light)

    # ── NWC ──────────────────────────────────────────────────────────────────
    ws_nwc = setup_sheet(wb, "NWC", "7B3F00")
    title_row(ws_nwc, 1, f"{company}  —  Net Working Capital")
    header_row(ws_nwc, 3, years)
    ar  = [r * dso / 365 for r in revenues]
    inv = [r * gross_margin * dio / 365 for r in revenues]
    ap  = [r * gross_margin * dpo / 365 for r in revenues]
    nwc = [a + inv_v - p for a, inv_v, p in zip(ar, inv, ap)]
    section(ws_nwc, 4, "WORKING CAPITAL")
    data_row(ws_nwc, 5, f"Trade Receivables AR ({unit})", ar)
    data_row(ws_nwc, 6, f"Inventories ({unit})", inv)
    data_row(ws_nwc, 7, f"Trade Payables AP ({unit})", ap)
    data_row(ws_nwc, 8, f"Net Working Capital ({unit})", nwc, bold=True, bg=fill_blue_light)
    chg_nwc = [nwc[0]] + [nwc[i] - nwc[i-1] for i in range(1, n)]
    data_row(ws_nwc, 9, f"Change in NWC ({unit})", chg_nwc)

    # ── CAPEX ─────────────────────────────────────────────────────────────────
    ws_cpx = setup_sheet(wb, "CAPEX", "2C4A6E")
    title_row(ws_cpx, 1, f"{company}  —  CAPEX Schedule")
    header_row(ws_cpx, 3, years)
    cpx_cfg = config.get("capex", {})
    maint = [cpx_cfg.get("maint_capex", 2000)] * n
    expan = [cpx_cfg.get("expan_capex", 5000)] * n
    total_cpx = [m + e for m, e in zip(maint, expan)]
    section(ws_cpx, 4, "CAPEX")
    data_row(ws_cpx, 5, f"Maintenance Capex ({unit})", maint)
    data_row(ws_cpx, 6, f"Expansion Capex ({unit})", expan)
    data_row(ws_cpx, 7, f"Total Capex ({unit})", total_cpx, bold=True, bg=fill_blue_light)

    # ── DEBT SCHEDULE ─────────────────────────────────────────────────────────
    ws_ds = setup_sheet(wb, "DEBT SCHEDULE", "A52A2A")
    title_row(ws_ds, 1, f"{company}  —  Debt Schedule")
    header_row(ws_ds, 3, years)
    opening_debt = [total_debt] + [max(total_debt - total_debt/n * i, 0) for i in range(1, n)]
    repayments = [total_debt / n] * n
    closing_debt = [o - r for o, r in zip(opening_debt, repayments)]
    interest_charges = [o * int_rate for o in opening_debt]
    section(ws_ds, 4, "DEBT WATERFALL")
    data_row(ws_ds, 5, f"Opening Debt ({unit})", opening_debt)
    data_row(ws_ds, 6, f"Repayments ({unit})", [-r for r in repayments])
    data_row(ws_ds, 7, f"Closing Debt ({unit})", closing_debt, bold=True, bg=fill_blue_light)
    data_row(ws_ds, 8, f"Interest Charge ({unit})", interest_charges)

    # ── CASH FLOW ────────────────────────────────────────────────────────────
    ws_cf = setup_sheet(wb, "CASH FLOW", "4A235A")
    title_row(ws_cf, 1, f"{company}  —  Cash Flow Statement")
    header_row(ws_cf, 3, years)
    op_cf = [e - c - t for e, c, t in zip(ebitdas, chg_nwc, taxes)]
    inv_cf = [-c for c in total_cpx]
    fin_cf = [-i - r for i, r in zip(interest_charges, repayments)]
    net_cf = [o + i + f for o, i, f in zip(op_cf, inv_cf, fin_cf)]
    closing_cash = []
    for i, nc in enumerate(net_cf):
        prev = closing_cash[i-1] if i > 0 else 0
        closing_cash.append(prev + nc)
    section(ws_cf, 4, "OPERATING")
    data_row(ws_cf, 5, f"Adj. EBITDA ({unit})", ebitdas)
    data_row(ws_cf, 6, f"Change in NWC ({unit})", [-c for c in chg_nwc])
    data_row(ws_cf, 7, f"Tax paid ({unit})", [-t for t in taxes])
    data_row(ws_cf, 8, f"Operating CF ({unit})", op_cf, bold=True, bg=fill_blue_light)
    section(ws_cf, 9, "INVESTING")
    data_row(ws_cf, 10, f"Capex ({unit})", inv_cf)
    data_row(ws_cf, 11, f"Free Cash Flow ({unit})", [o + i for o, i in zip(op_cf, inv_cf)], bold=True, bg=fill_blue_light)
    section(ws_cf, 12, "FINANCING")
    data_row(ws_cf, 13, f"Interest paid ({unit})", [-i for i in interest_charges])
    data_row(ws_cf, 14, f"Debt repayments ({unit})", [-r for r in repayments])
    data_row(ws_cf, 15, f"Net Movement ({unit})", net_cf)
    data_row(ws_cf, 16, f"Closing Cash ({unit})", closing_cash, bold=True, bg=fill_blue_light)

    # ── KPIs ─────────────────────────────────────────────────────────────────
    ws_kpi = setup_sheet(wb, "KPIs & RATIOS", "1E4D2B")
    title_row(ws_kpi, 1, f"{company}  —  KPIs & Financial Ratios")
    header_row(ws_kpi, 3, years)
    section(ws_kpi, 4, "PROFITABILITY")
    data_row(ws_kpi, 5, "Revenue growth %", [rev_growth]*n, fmt=FMT_PCT1)
    data_row(ws_kpi, 6, "Gross margin %", [g/r for g,r in zip(gross_profits,revenues)], fmt=FMT_PCT1)
    data_row(ws_kpi, 7, "EBITDA margin %", [e/r for e,r in zip(ebitdas,revenues)], fmt=FMT_PCT1)
    data_row(ws_kpi, 8, "Net margin %", [ni/r for ni,r in zip(net_incomes,revenues)], fmt=FMT_PCT1)
    section(ws_kpi, 9, "LEVERAGE")
    net_debt = [cd - cc for cd, cc in zip(closing_debt, closing_cash)]
    data_row(ws_kpi, 10, f"Net Debt ({unit})", net_debt)
    data_row(ws_kpi, 11, "Net Leverage (ND/EBITDA)", [nd/e if e else 0 for nd,e in zip(net_debt,ebitdas)], fmt=FMT_MULT)
    data_row(ws_kpi, 12, "ICR (EBITDA/Interest)", [e/i if i else 0 for e,i in zip(ebitdas,interest_charges)], fmt=FMT_MULT)

    # ── OUTPUT PRINT ─────────────────────────────────────────────────────────
    ws_out = setup_sheet(wb, "OUTPUT", "0D1B3E")
    ws_out.sheet_view.zoomScale = 85
    ws_out.page_setup.paperSize = 9  # A4
    ws_out.page_setup.orientation = "landscape"
    ws_out.page_setup.fitToPage = True
    title_row(ws_out, 1, f"{company}  —  Business Plan Summary")
    header_row(ws_out, 3, years)
    section(ws_out, 4, "INCOME STATEMENT SUMMARY")
    data_row(ws_out, 5, f"Net Revenue ({unit})", revenues, bold=True)
    data_row(ws_out, 6, "Growth %", [0] + [(revenues[i]-revenues[i-1])/revenues[i-1] for i in range(1,n)], fmt=FMT_PCT1)
    data_row(ws_out, 7, f"Gross Profit ({unit})", gross_profits)
    data_row(ws_out, 8, "Gross Margin %", [g/r for g,r in zip(gross_profits,revenues)], fmt=FMT_PCT1)
    data_row(ws_out, 9, f"Adj. EBITDA ({unit})", ebitdas, bold=True, bg=fill_blue_light)
    data_row(ws_out, 10, "EBITDA Margin %", [e/r for e,r in zip(ebitdas,revenues)], fmt=FMT_PCT1)
    data_row(ws_out, 11, f"Net Income ({unit})", net_incomes)
    section(ws_out, 13, "CASH FLOW SUMMARY")
    data_row(ws_out, 14, f"Operating CF ({unit})", op_cf)
    data_row(ws_out, 15, f"Free Cash Flow ({unit})", [o+i for o,i in zip(op_cf,inv_cf)], bold=True, bg=fill_blue_light)
    data_row(ws_out, 16, f"Closing Cash ({unit})", closing_cash)
    section(ws_out, 18, "LEVERAGE SUMMARY")
    data_row(ws_out, 19, f"Gross Debt ({unit})", closing_debt)
    data_row(ws_out, 20, f"Net Debt ({unit})", net_debt, bold=True)
    data_row(ws_out, 21, "Net Leverage (x)", [nd/e if e else 0 for nd,e in zip(net_debt,ebitdas)], fmt=FMT_MULT)

    wb.save(output_path)
    return output_path
