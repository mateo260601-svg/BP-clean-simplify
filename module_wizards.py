from typing import Dict, Any, List

BP_WIZARD_SECTIONS = [
    {
        "id": "company",
        "title": "1. Company & Transaction Context",
        "duration_min": 10,
        "fields": [
            "company_name", "sector", "currency", "country", "deal_type",
            "transaction_rationale", "ownership", "management_team",
            "business_description", "investment_thesis"
        ],
    },
    {
        "id": "historical_financials",
        "title": "2. Historical Financials",
        "duration_min": 15,
        "fields": [
            "historical_revenue", "historical_gross_profit", "historical_ebitda",
            "historical_ebit", "historical_net_income", "historical_cash",
            "historical_debt", "historical_capex", "audit_adjustments",
            "normalisations"
        ],
    },
    {
        "id": "revenue_build",
        "title": "3. Revenue Build-Up",
        "duration_min": 20,
        "fields": [
            "revenue_streams", "volume_assumptions", "price_assumptions",
            "mix_effect", "customer_retention", "churn", "new_business_pipeline",
            "contracted_revenue", "recurring_revenue", "cyclicality", "seasonality"
        ],
    },
    {
        "id": "operations",
        "title": "4. Operations & Capacity",
        "duration_min": 15,
        "fields": [
            "capacity", "utilisation", "production_sites", "fte",
            "productivity", "fixed_cost_base", "variable_cost_base",
            "operating_leverage"
        ],
    },
    {
        "id": "gross_margin",
        "title": "5. Gross Margin & COGS",
        "duration_min": 15,
        "fields": [
            "raw_materials", "direct_labor", "freight", "energy",
            "supplier_terms", "procurement_savings", "price_cost_lag",
            "gross_margin_target"
        ],
    },
    {
        "id": "opex",
        "title": "6. SG&A / Opex",
        "duration_min": 15,
        "fields": [
            "sales_marketing", "general_admin", "rd", "rent", "it_costs",
            "insurance", "professional_fees", "management_costs", "cost_savings"
        ],
    },
    {
        "id": "working_capital",
        "title": "7. Working Capital",
        "duration_min": 15,
        "fields": [
            "dso", "dio", "dpo", "inventory_policy", "customer_payment_terms",
            "supplier_payment_terms", "seasonality", "factoring",
            "working_capital_normalisation"
        ],
    },
    {
        "id": "capex",
        "title": "8. Capex & Asset Base",
        "duration_min": 15,
        "fields": [
            "maintenance_capex", "growth_capex", "expansion_projects",
            "useful_life", "opening_ppe", "depreciation_policy",
            "asset_replacement_cycle"
        ],
    },
    {
        "id": "debt",
        "title": "9. Debt & Financing",
        "duration_min": 15,
        "fields": [
            "opening_debt", "interest_rate", "amortisation", "cash_sweep",
            "covenants", "leases", "debt_like_items", "refinancing_assumptions"
        ],
    },
    {
        "id": "tax",
        "title": "10. Tax & Legal",
        "duration_min": 10,
        "fields": [
            "tax_rate", "nols", "cash_tax", "deferred_tax",
            "legal_claims", "contingent_liabilities"
        ],
    },
    {
        "id": "scenarios",
        "title": "11. Scenarios & Sensitivities",
        "duration_min": 20,
        "fields": [
            "base_case", "downside_case", "upside_case", "price_sensitivity",
            "volume_sensitivity", "margin_sensitivity", "covenant_sensitivity"
        ],
    },
    {
        "id": "outputs",
        "title": "12. Outputs & Review",
        "duration_min": 15,
        "fields": [
            "management_case_review", "bank_case_review", "ic_case_review",
            "key_diligence_questions", "investment_committee_messages"
        ],
    },
]

MODULE_SETUP_TIMES = {
    "bp": {"v1_hours": 1, "institutional_hours": "2-6"},
    "im_deck": {"v1_hours": "1-2", "institutional_hours": "4-12"},
    "qoe": {"v1_hours": "1-3", "institutional_hours": "1-3 days"},
    "restructuring": {"v1_hours": "2-4", "institutional_hours": "1-2 days"},
}

DEFAULT_INSTITUTIONAL_INTAKE = {
    "company_name": "Target Company",
    "sector": "Industrial / Manufacturing",
    "currency": "EUR",
    "country": "France",
    "deal_type": "M&A",
    "start_year": 2026,
    "forecast_years": 5,
    "historical_years": 3,

    "revenue": 202000,
    "revenue_growth": 0.073,
    "contracted_revenue_pct": 0.34,
    "volume_growth": 0.05,
    "price_growth": 0.02,
    "churn": 0.03,
    "new_business_growth": 0.06,

    "gross_margin": 0.391,
    "raw_material_pct_sales": 0.45,
    "direct_labor_pct_sales": 0.08,
    "freight_pct_sales": 0.03,
    "energy_pct_sales": 0.025,

    "ebitda_margin": 0.229,
    "sgna_pct_sales": 0.11,
    "fixed_costs": 18000,
    "variable_opex_pct_sales": 0.06,

    "cash": 18700,
    "debt": 201000,
    "interest_rate": 0.075,
    "tax_rate": 0.25,

    "dso": 55,
    "dio": 40,
    "dpo": 55,

    "maintenance_capex": 11500,
    "growth_capex": 0,
    "opening_ppe": 85000,
    "useful_life": 20,

    "capacity": 432000,
    "utilisation": 0.51,
    "fte": 86,

    "investment_thesis": "",
    "value_creation_plan": "",
    "key_risks": "",
    "diligence_questions": "",
}
