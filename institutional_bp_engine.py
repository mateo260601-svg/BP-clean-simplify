from typing import Dict, Any, List
from copy import deepcopy
from module_wizards import DEFAULT_INSTITUTIONAL_INTAKE

def _float(v, default=0.0):
    try:
        if v in [None, ""]:
            return default
        if isinstance(v, str):
            v = v.replace("%", "").replace(",", ".").replace(" ", "")
        return float(v)
    except Exception:
        return default

def _pct(v, default=0.0):
    n = _float(v, default)
    return n / 100 if n > 1 else n

def clean_intake(intake: Dict[str, Any]) -> Dict[str, Any]:
    x = deepcopy(DEFAULT_INSTITUTIONAL_INTAKE)
    x.update(intake or {})
    pct_fields = [
        "revenue_growth", "contracted_revenue_pct", "volume_growth", "price_growth", "churn",
        "new_business_growth", "gross_margin", "raw_material_pct_sales", "direct_labor_pct_sales",
        "freight_pct_sales", "energy_pct_sales", "ebitda_margin", "sgna_pct_sales",
        "variable_opex_pct_sales", "interest_rate", "tax_rate", "utilisation"
    ]
    for f in pct_fields:
        x[f] = _pct(x.get(f), DEFAULT_INSTITUTIONAL_INTAKE.get(f, 0.0))
    numeric_fields = [
        "revenue", "cash", "debt", "dso", "dio", "dpo", "maintenance_capex", "growth_capex",
        "opening_ppe", "useful_life", "capacity", "fte", "fixed_costs", "start_year",
        "forecast_years", "historical_years"
    ]
    for f in numeric_fields:
        x[f] = _float(x.get(f), DEFAULT_INSTITUTIONAL_INTAKE.get(f, 0.0))
    x["forecast_years"] = int(x["forecast_years"])
    x["historical_years"] = int(x["historical_years"])
    x["start_year"] = int(x["start_year"])
    return x

def build_projection(intake: Dict[str, Any]) -> Dict[str, Any]:
    x = clean_intake(intake)
    years = [x["start_year"] + i for i in range(x["forecast_years"])]
    rows = []
    revenue = x["revenue"]
    debt = x["debt"]
    cash = x["cash"]
    opening_ppe = x["opening_ppe"]

    for i, year in enumerate(years):
        if i > 0:
            revenue *= (1 + x["revenue_growth"])
        volume_growth = x["volume_growth"]
        price_growth = x["price_growth"]
        contracted_revenue = revenue * x["contracted_revenue_pct"]
        new_business = revenue * x["new_business_growth"]
        churn_impact = revenue * x["churn"]

        gross_profit = revenue * x["gross_margin"]
        raw_materials = revenue * x["raw_material_pct_sales"]
        direct_labor = revenue * x["direct_labor_pct_sales"]
        freight = revenue * x["freight_pct_sales"]
        energy = revenue * x["energy_pct_sales"]
        sgna = revenue * x["sgna_pct_sales"]
        variable_opex = revenue * x["variable_opex_pct_sales"]
        ebitda = revenue * x["ebitda_margin"]
        depreciation = opening_ppe / max(x["useful_life"], 1)
        ebit = ebitda - depreciation
        interest = debt * x["interest_rate"]
        pbt = ebit - interest
        tax = max(pbt, 0) * x["tax_rate"]
        net_income = pbt - tax

        receivables = revenue * x["dso"] / 365
        inventory = revenue * x["dio"] / 365
        payables = revenue * x["dpo"] / 365
        nwc = receivables + inventory - payables
        capex = x["maintenance_capex"] + x["growth_capex"]
        fcf = ebitda - tax - capex - (nwc * 0.05)
        cash += fcf
        debt = max(0, debt - max(fcf * 0.5, 0))
        net_debt = debt - cash
        utilisation = min(1.0, x["utilisation"] + i * 0.05)
        capacity_used = x["capacity"] * utilisation

        rows.append({
            "year": year,
            "revenue": revenue,
            "contracted_revenue": contracted_revenue,
            "new_business": new_business,
            "churn_impact": churn_impact,
            "volume_growth": volume_growth,
            "price_growth": price_growth,
            "gross_profit": gross_profit,
            "raw_materials": raw_materials,
            "direct_labor": direct_labor,
            "freight": freight,
            "energy": energy,
            "sgna": sgna,
            "variable_opex": variable_opex,
            "ebitda": ebitda,
            "depreciation": depreciation,
            "ebit": ebit,
            "interest": interest,
            "pbt": pbt,
            "tax": tax,
            "net_income": net_income,
            "receivables": receivables,
            "inventory": inventory,
            "payables": payables,
            "nwc": nwc,
            "capex": capex,
            "fcf": fcf,
            "cash": cash,
            "debt": debt,
            "net_debt": net_debt,
            "net_debt_ebitda": net_debt / ebitda if ebitda else None,
            "ebitda_margin": ebitda / revenue if revenue else None,
            "fcf_conversion": fcf / ebitda if ebitda else None,
            "utilisation": utilisation,
            "capacity_used": capacity_used,
            "fte": x["fte"],
            "revenue_per_fte": revenue / x["fte"] if x["fte"] else None,
        })

    return {"intake": x, "projection": rows}

def build_scenarios(intake: Dict[str, Any]) -> Dict[str, Any]:
    base = clean_intake(intake)
    cases = {}
    for name, rev_delta, margin_delta in [
        ("Downside", -0.04, -0.03),
        ("Base", 0.0, 0.0),
        ("Upside", 0.04, 0.03),
    ]:
        c = deepcopy(base)
        c["revenue_growth"] = max(-0.20, c["revenue_growth"] + rev_delta)
        c["ebitda_margin"] = max(0.0, c["ebitda_margin"] + margin_delta)
        cases[name] = build_projection(c)
    return cases

def to_legacy_build_config(intake: Dict[str, Any]) -> Dict[str, Any]:
    x = clean_intake(intake)
    return {
        "company_name": x["company_name"],
        "currency": x["currency"],
        "business_type": "industrial",
        "sector": x["sector"],
        "scenarios": "all",
        "n_years": x["forecast_years"],
        "start_year": x["start_year"],
        "actuals_months": 0,
        "opening_cash": x["cash"],
        "base_revenue": x["revenue"],
        "revenue_growth": x["revenue_growth"],
        "gross_margin": x["gross_margin"],
        "ebitda_margin": x["ebitda_margin"],
        "dso": x["dso"],
        "dio": x["dio"],
        "dio_rm": max(0, x["dio"] - 10),
        "dpo": x["dpo"],
        "tax_rate": x["tax_rate"],
        "inflation": 0.025,
        "price_per_mt": 2000,
        "capacity_mt": x["capacity"],
        "capex": {
            "opening_ppe": x["opening_ppe"],
            "maint_capex": x["maintenance_capex"],
            "expan_capex": x["growth_capex"],
            "useful_life": int(x["useful_life"]),
        },
        "debt": {
            "total_debt": x["debt"],
            "interest_rate": x["interest_rate"],
            "tranches": [{
                "name": "Senior Debt",
                "type": "Term Loan",
                "amount": x["debt"],
                "rate": x["interest_rate"],
                "tenor": x["forecast_years"],
                "amortization": "cash_sweep"
            }]
        },
        "client_setup": {
            "investment_thesis": x.get("investment_thesis", ""),
            "value_creation_plan": x.get("value_creation_plan", ""),
            "key_risks": x.get("key_risks", ""),
            "diligence_questions": x.get("diligence_questions", ""),
            "raw_intake": x
        }
    }
