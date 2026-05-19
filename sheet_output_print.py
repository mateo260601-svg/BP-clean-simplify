import sys
import json
from openpyxl import Workbook
from periods import build_periods
from sheet_config       import build_config
from sheet_assumptions  import build_assumptions
from sheet_pl           import build_pl
from sheet_debt         import build_debt_schedule
from sheet_others       import (build_nwc, build_capex, build_balance_sheet,
                                build_cash_flow, build_kpis, build_checks)
from sheet_output_print import build_output_print

# 
# DEFAULT CONFIGURATION  JBF Industrial / Restructuring archetype
# 
DEFAULT_CONFIG = {
    "company_name":       "JBF Global Europe  Industrial BP",
    "business_type":      "Industriel / Restructuring",
    "currency":           "USD",
    "units":              "k",
    "fy_start_month":     4,        # April fiscal year start
    "proj_start_year":    2025,
    "n_years":            7,
    "actuals_end_year":   2024,
    "actuals_end_month":  3,
    "freq":               "Annual",

    "modules": {
        "debt":       1,
        "tax":        1,
        "scenarios":  1,
        "returns":    0,
        "valuation":  0,
        "consol":     0,
    },

    "revenue": {
        "capacity_mt":    [220000]*7,
        "base_volume":    [180000, 190000, 200000, 205000, 210000, 215000, 215000],
        "volume_growth":  [0.00,   0.056,  0.053,  0.025,  0.024,  0.024,  0.000],
        "price_per_mt":   [1050,   1080,   1100,   1120,   1130,   1140,   1150],
        "freight_mt":     [35]*7,
        "commission_pct": [0.01]*7,
    },

    "costs": {
        "direct_mat_mt":    [520, 535, 548, 558, 565, 572, 578],
        "direct_mat_gr":    [0.00, 0.029, 0.024, 0.018, 0.013, 0.012, 0.010],
        "utilities_mt":     [45]*7,
        "packing_mt":       [18]*7,
        "var_opex_other_mt":[12]*7,
        "staff_prod":       [8500, 8670, 8843, 9020, 9200, 9384, 9384],
        "staff_sga":        [3200, 3264, 3329, 3396, 3464, 3533, 3533],
        "headcount_gr":     [0.02]*7,
        "maintenance":      [2400, 2450, 2500, 2550, 2600, 2650, 2650],
        "insurance":        [800]*7,
        "rent":             [600]*7,
        "it":               [400]*7,
        "prof_fees":        [350]*7,
        "other_sga":        [500]*7,
        "restr":            [2000, 1000, 0, 0, 0, 0, 0],
    },

    "nwc": {
        "dso": [50]*7,
        "dio": [35]*7,
        "dpo": [55]*7,
        "oca_pct": [0.01]*7,
        "ocl_pct": [0.02]*7,
    },

    "capex": {
        "maint":          [3500, 3500, 3500, 3500, 3500, 3500, 3500],
        "expan":          [12000, 8000, 4000, 2000, 1500, 1500, 1500],
        "opening_ppe":    95000,
        "useful_life":    20,
        "accum_dep_open": 28000,
    },

    "tax": {
        "rate":          [0.25]*7,
        "loss_cf_open":  15000,
        "dt_rate":       [0.25]*7,
    },

    "macro": {
        "cpi":         [0.025]*7,
        "fx_usd_eur":  [1.09]*7,
        "fx_usd_gbp":  [1.27]*7,
        "fx_usd_aed":  [3.67]*7,
    },

    #  Active debt tranches 
    "debt": {
        "tla": {"active": 1, "amount": 130000, "currency": "USD",
                "tenor_yrs": 7, "margin_pct": 0.0325, "pik_margin_pct": 0.0},
        "ss":  {"active": 1, "amount": 20000,  "currency": "USD",
                "tenor_yrs": 3, "margin_pct": 0.0450, "pik_margin_pct": 0.0},
        "rcf": {"active": 1, "amount": 40000,  "currency": "USD",
                "tenor_yrs": 5, "margin_pct": 0.0325, "pik_margin_pct": 0.0},
        "mur": {"active": 1, "amount": 55000,  "currency": "USD",
                "tenor_yrs": 7, "margin_pct": 0.0340, "pik_margin_pct": 0.0},
        "tlb": {"active": 0, "amount": 0},
        "mez": {"active": 0, "amount": 0},
        "pik": {"active": 0, "amount": 0},
        "shl": {"active": 0, "amount": 0},
    },

    "debt_mechanics": {
        "base_rate_index":    "SOFR",
        "base_rate_pct":      0.045,
        "base_rate_floor":    0.0,
        "tla_margin":         0.0325,
        "tlb_margin":         0.0400,
        "mezz_cash_margin":   0.0700,
        "mezz_pik_margin":    0.0400,
        "upfront_fee_pct":    0.015,
        "commit_fee_pct":     0.005,
        "oid_pct":            0.0,
        "cash_sweep_pct":     0.75,
        "cash_sweep_active":  1,
        "margin_ratchet":     0,
        "covenant_tracking":  1,
        "lev_covenant":       5.5,
        "icr_covenant":       2.0,
        "dscr_covenant":      0.0,
        "fx_hedge":           0,
        "irs_active":         0,
    },
}

def build_workbook(config=None, output_path=None):
    if config is None:
        config = DEFAULT_CONFIG

    n = config["n_years"]
    sy = config["proj_start_year"]
    sm = config["fy_start_month"]
    ay = config["actuals_end_year"]
    am = config["actuals_end_month"]

    monthly_periods, years = build_periods(sy, sm, n, ay, am)

    wb = Workbook()
    # Remove default sheet
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

    row_map = {}

    print("Building CONFIG...")
    build_config(wb, config)

    print("Building ASSUMPTIONS...")
    build_assumptions(wb, config, years, monthly_periods)

    print("Building P&L...")
    build_pl(wb, config, years, row_map)

    print("Building NWC...")
    build_nwc(wb, config, years, row_map)

    print("Building CAPEX...")
    build_capex(wb, config, years, row_map)

    print("Building BALANCE SHEET...")
    build_balance_sheet(wb, config, years, row_map)

    print("Building CASH FLOW...")
    build_cash_flow(wb, config, years, row_map)

    print("Building DEBT SCHEDULE...")
    build_debt_schedule(wb, config, years, row_map)

    print("Building KPIs & RATIOS...")
    build_kpis(wb, config, years, row_map)

    print("Building CHECKS...")
    build_checks(wb, config, years, row_map)

    print("Building OUTPUT (PRINT)...")
    build_output_print(wb, config, years, row_map)

    #  Sheet ordering 
    desired_order = [
        "CONFIG", "ASSUMPTIONS", "P&L", "NWC", "CAPEX",
        "BALANCE SHEET", "CASH FLOW", "DEBT SCHEDULE",
        "KPIs & RATIOS", "CHECKS", "OUTPUT (PRINT)",
    ]
    wb._sheets.sort(
        key=lambda s: desired_order.index(s.title) if s.title in desired_order else 99
    )

    if output_path is None:
        output_path = "/home/claude/bp_generator/BP_GENERATOR_v1.xlsx"

    wb.save(output_path)
    print(f"\n  Saved  {output_path}")
    return output_path

if __name__ == "__main__":
    path = build_workbook()
    print(f"Done: {path}")
