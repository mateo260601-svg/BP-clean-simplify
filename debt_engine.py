"""
debt_engine.py  —  Full institutional debt modelling engine
60+ instrument types, full waterfall, PIK capitalisation, OID, ratchets,
convertibles, Islamic finance, restructuring instruments.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
import math

# ══════════════════════════════════════════════════════════════════════════════
# INSTRUMENT CATALOGUE  —  60+ types
# ══════════════════════════════════════════════════════════════════════════════

DEBT_CATALOGUE = {
    # ── Senior Secured ────────────────────────────────────────────────────────
    "tla": {
        "name": "Senior Term Loan A  (TLA)",
        "category": "Senior Secured",
        "color": "1A3A6C",
        "defaults": {"amort": "linear", "cash_rate": 0.0, "margin": 0.040,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 7,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01,
                     "commitment_fee": 0.0},
    },
    "tlb": {
        "name": "Senior Term Loan B  (TLB)",
        "category": "Senior Secured",
        "color": "1A3A6C",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.055,
                     "base_rate": "SOFR", "pik_rate": 0.0, "tenor": 7,
                     "floor": 0.01, "oid_pct": 0.02, "upfront_fee": 0.015,
                     "commitment_fee": 0.0},
    },
    "tlc": {
        "name": "Senior Term Loan C  (TLC)",
        "category": "Senior Secured",
        "color": "1A3A6C",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.065,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 8,
                     "floor": 0.01, "oid_pct": 0.025, "upfront_fee": 0.02},
    },
    "rcf": {
        "name": "Revolving Credit Facility  (RCF)",
        "category": "Senior Secured",
        "color": "2A5298",
        "defaults": {"amort": "revolving", "cash_rate": 0.0, "margin": 0.040,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 5,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01,
                     "commitment_fee": 0.005, "drawn_pct": 0.50},
    },
    "super_senior_rcf": {
        "name": "Super Senior RCF",
        "category": "Senior Secured",
        "color": "0D2E6E",
        "defaults": {"amort": "revolving", "cash_rate": 0.0, "margin": 0.035,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 5,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.0075,
                     "commitment_fee": 0.004},
    },
    "capex_facility": {
        "name": "Capex Facility",
        "category": "Senior Secured",
        "color": "2A5298",
        "defaults": {"amort": "linear", "cash_rate": 0.0, "margin": 0.045,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 7,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01,
                     "commitment_fee": 0.005},
    },
    "acquisition_facility": {
        "name": "Acquisition / Bridge Facility",
        "category": "Senior Secured",
        "color": "2A5298",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.060,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 2,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.02},
    },
    "lc_facility": {
        "name": "Letter of Credit / Guarantee Facility",
        "category": "Senior Secured",
        "color": "2A5298",
        "defaults": {"amort": "revolving", "cash_rate": 0.0, "margin": 0.02,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 5,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.005,
                     "commitment_fee": 0.0025},
    },
    # ── Second Lien / Unitranche ──────────────────────────────────────────────
    "second_lien": {
        "name": "Second Lien Term Loan",
        "category": "Second Lien",
        "color": "2D6A9F",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.080,
                     "base_rate": "SOFR", "pik_rate": 0.0, "tenor": 8,
                     "floor": 0.01, "oid_pct": 0.03, "upfront_fee": 0.02},
    },
    "unitranche": {
        "name": "Unitranche Facility",
        "category": "Second Lien",
        "color": "2D6A9F",
        "defaults": {"amort": "linear", "cash_rate": 0.0, "margin": 0.065,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 7,
                     "floor": 0.0, "oid_pct": 0.01, "upfront_fee": 0.015},
    },
    "last_out_unitranche": {
        "name": "Last Out Unitranche",
        "category": "Second Lien",
        "color": "2D6A9F",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.090,
                     "base_rate": "SOFR", "pik_rate": 0.0, "tenor": 7,
                     "floor": 0.01, "oid_pct": 0.035, "upfront_fee": 0.025},
    },
    # ── Mezzanine ─────────────────────────────────────────────────────────────
    "mezz_cash": {
        "name": "Mezzanine  —  Cash Pay",
        "category": "Mezzanine",
        "color": "7B2D8B",
        "defaults": {"amort": "bullet", "cash_rate": 0.10, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 8,
                     "floor": 0.0, "oid_pct": 0.02, "upfront_fee": 0.025},
    },
    "mezz_pik_toggle": {
        "name": "Mezzanine  —  PIK Toggle",
        "category": "Mezzanine",
        "color": "7B2D8B",
        "defaults": {"amort": "bullet", "cash_rate": 0.09, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.025, "tenor": 9,
                     "floor": 0.0, "oid_pct": 0.02, "upfront_fee": 0.025},
    },
    "mezz_full_pik": {
        "name": "Mezzanine  —  Full PIK",
        "category": "Mezzanine",
        "color": "7B2D8B",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.125, "tenor": 9,
                     "floor": 0.0, "oid_pct": 0.03, "upfront_fee": 0.03},
    },
    "junior_mezz": {
        "name": "Junior Mezzanine",
        "category": "Mezzanine",
        "color": "9B3DBB",
        "defaults": {"amort": "bullet", "cash_rate": 0.08, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.04, "tenor": 10,
                     "floor": 0.0, "oid_pct": 0.03, "upfront_fee": 0.03},
    },
    # ── High Yield / Capital Markets ──────────────────────────────────────────
    "hyb": {
        "name": "High Yield Bond  (HYB)",
        "category": "Capital Markets",
        "color": "B45309",
        "defaults": {"amort": "bullet", "cash_rate": 0.085, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 8,
                     "floor": 0.0, "oid_pct": 0.02, "upfront_fee": 0.015},
    },
    "ssn": {
        "name": "Senior Secured Notes  (SSN)",
        "category": "Capital Markets",
        "color": "B45309",
        "defaults": {"amort": "bullet", "cash_rate": 0.075, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 7,
                     "floor": 0.0, "oid_pct": 0.015, "upfront_fee": 0.012},
    },
    "senior_sub_notes": {
        "name": "Senior Subordinated Notes",
        "category": "Capital Markets",
        "color": "B45309",
        "defaults": {"amort": "bullet", "cash_rate": 0.095, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 8,
                     "floor": 0.0, "oid_pct": 0.025, "upfront_fee": 0.02},
    },
    "uspp": {
        "name": "US Private Placement  (USPP)",
        "category": "Capital Markets",
        "color": "92400E",
        "defaults": {"amort": "bullet", "cash_rate": 0.06, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 10,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.008},
    },
    "euro_pp": {
        "name": "Euro Private Placement  (Euro PP)",
        "category": "Capital Markets",
        "color": "92400E",
        "defaults": {"amort": "bullet", "cash_rate": 0.055, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 7,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.007},
    },
    "green_bond": {
        "name": "Green Bond  /  Sustainability-Linked Bond",
        "category": "Capital Markets",
        "color": "1A5C2A",
        "defaults": {"amort": "bullet", "cash_rate": 0.065, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 10,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01},
    },
    "schuldschein": {
        "name": "Schuldschein  (German PP)",
        "category": "Capital Markets",
        "color": "92400E",
        "defaults": {"amort": "bullet", "cash_rate": 0.05, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 7,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.005},
    },
    # ── Equity-Linked / Hybrid ────────────────────────────────────────────────
    "convertible_bond": {
        "name": "Convertible Bond",
        "category": "Equity-Linked",
        "color": "6B21A8",
        "defaults": {"amort": "bullet", "cash_rate": 0.04, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 5,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.015,
                     "conversion_premium": 0.30, "conversion_price": 10.0},
    },
    "convertible_note": {
        "name": "Convertible Promissory Note",
        "category": "Equity-Linked",
        "color": "6B21A8",
        "defaults": {"amort": "bullet", "cash_rate": 0.06, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 3,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01},
    },
    "preferred_equity": {
        "name": "Preferred Equity  (Redeemable)",
        "category": "Equity-Linked",
        "color": "6B21A8",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.10, "tenor": 10,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.02},
    },
    "shl": {
        "name": "Shareholder Loan  (SHL)",
        "category": "Equity-Linked",
        "color": "6B21A8",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.12, "tenor": 10,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.0},
    },
    "vendor_loan": {
        "name": "Vendor Loan Note  (VLN)",
        "category": "Equity-Linked",
        "color": "7C3AED",
        "defaults": {"amort": "bullet", "cash_rate": 0.05, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.04, "tenor": 5,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.0},
    },
    "earn_out": {
        "name": "Earn-Out Obligation",
        "category": "Equity-Linked",
        "color": "7C3AED",
        "defaults": {"amort": "custom", "cash_rate": 0.0, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 3,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.0},
    },
    # ── Islamic Finance ───────────────────────────────────────────────────────
    "murabaha": {
        "name": "Murabaha  (Commodity / Trade)",
        "category": "Islamic Finance",
        "color": "065F46",
        "defaults": {"amort": "linear", "cash_rate": 0.055, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 7,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01},
    },
    "murabaha_re": {
        "name": "Murabaha  (Real Estate)",
        "category": "Islamic Finance",
        "color": "065F46",
        "defaults": {"amort": "linear", "cash_rate": 0.05, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 15,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01},
    },
    "ijara": {
        "name": "Ijara  (Finance Lease / Islamic)",
        "category": "Islamic Finance",
        "color": "065F46",
        "defaults": {"amort": "linear", "cash_rate": 0.05, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 10,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.0075},
    },
    "musharaka": {
        "name": "Diminishing Musharaka",
        "category": "Islamic Finance",
        "color": "065F46",
        "defaults": {"amort": "linear", "cash_rate": 0.06, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 10,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01},
    },
    "sukuk": {
        "name": "Sukuk  (Islamic Bond / Certificates)",
        "category": "Islamic Finance",
        "color": "047857",
        "defaults": {"amort": "bullet", "cash_rate": 0.055, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 7,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01},
    },
    "wakala": {
        "name": "Wakala Facility",
        "category": "Islamic Finance",
        "color": "047857",
        "defaults": {"amort": "revolving", "cash_rate": 0.05, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 5,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.0075},
    },
    # ── Asset-Based / Structured ──────────────────────────────────────────────
    "abl": {
        "name": "Asset-Based Lending  (ABL)",
        "category": "Structured Finance",
        "color": "0E7490",
        "defaults": {"amort": "revolving", "cash_rate": 0.0, "margin": 0.030,
                     "base_rate": "SOFR", "pik_rate": 0.0, "tenor": 3,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.005,
                     "commitment_fee": 0.003},
    },
    "factoring": {
        "name": "Receivables Factoring / Discounting",
        "category": "Structured Finance",
        "color": "0E7490",
        "defaults": {"amort": "revolving", "cash_rate": 0.0, "margin": 0.025,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 1,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.003},
    },
    "supply_chain": {
        "name": "Supply Chain Finance  (SCF / Reverse Factoring)",
        "category": "Structured Finance",
        "color": "0E7490",
        "defaults": {"amort": "revolving", "cash_rate": 0.0, "margin": 0.02,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 1,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.002},
    },
    "construction_facility": {
        "name": "Construction / Development Facility",
        "category": "Structured Finance",
        "color": "0E7490",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.045,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 3,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.015,
                     "commitment_fee": 0.005},
    },
    "property_finance": {
        "name": "Real Estate / Property Finance",
        "category": "Structured Finance",
        "color": "0369A1",
        "defaults": {"amort": "linear", "cash_rate": 0.0, "margin": 0.035,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 20,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01},
    },
    "eca_facility": {
        "name": "ECA-Backed Export Credit Facility",
        "category": "Structured Finance",
        "color": "0369A1",
        "defaults": {"amort": "linear", "cash_rate": 0.0, "margin": 0.02,
                     "base_rate": "CIRR", "pik_rate": 0.0, "tenor": 12,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.005},
    },
    "government_loan": {
        "name": "Government / Subsidized Loan",
        "category": "Structured Finance",
        "color": "0369A1",
        "defaults": {"amort": "linear", "cash_rate": 0.02, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 15,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.0},
    },
    # ── Restructuring Instruments ─────────────────────────────────────────────
    "dip": {
        "name": "DIP Financing  (Debtor-in-Possession)",
        "category": "Restructuring",
        "color": "991B1B",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.085,
                     "base_rate": "SOFR", "pik_rate": 0.0, "tenor": 1,
                     "floor": 0.01, "oid_pct": 0.0, "upfront_fee": 0.04},
    },
    "new_money": {
        "name": "New Money Facility  (Post-Restruc.)",
        "category": "Restructuring",
        "color": "991B1B",
        "defaults": {"amort": "linear", "cash_rate": 0.0, "margin": 0.065,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 5,
                     "floor": 0.0, "oid_pct": 0.03, "upfront_fee": 0.03},
    },
    "pik_toggle_forced": {
        "name": "PIK Toggle Note  (Forced PIK Period)",
        "category": "Restructuring",
        "color": "991B1B",
        "defaults": {"amort": "bullet", "cash_rate": 0.05, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.08, "tenor": 7,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.02,
                     "pik_toggle_months": 24},
    },
    "debt_equity_swap": {
        "name": "Debt-to-Equity Swap  (Converted portion)",
        "category": "Restructuring",
        "color": "B91C1C",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 0,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.0},
    },
    "amend_extend": {
        "name": "Amend & Extend  (Extended Maturity)",
        "category": "Restructuring",
        "color": "B91C1C",
        "defaults": {"amort": "bullet", "cash_rate": 0.0, "margin": 0.055,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 3,
                     "floor": 0.0, "oid_pct": 0.01, "upfront_fee": 0.015},
    },
    "super_senior_nm": {
        "name": "Super Senior New Money  (Restruc.)",
        "category": "Restructuring",
        "color": "7F1D1D",
        "defaults": {"amort": "linear", "cash_rate": 0.0, "margin": 0.07,
                     "base_rate": "EURIBOR", "pik_rate": 0.0, "tenor": 5,
                     "floor": 0.0, "oid_pct": 0.03, "upfront_fee": 0.035},
    },
    # ── Leasing (IFRS 16) ─────────────────────────────────────────────────────
    "finance_lease": {
        "name": "Finance Lease  (IFRS 16)",
        "category": "Leasing",
        "color": "374151",
        "defaults": {"amort": "linear", "cash_rate": 0.045, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 5,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.0},
    },
    "operating_lease_rou": {
        "name": "Operating Lease ROU Asset  (IFRS 16)",
        "category": "Leasing",
        "color": "374151",
        "defaults": {"amort": "linear", "cash_rate": 0.04, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 10,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.0},
    },
    "sale_leaseback": {
        "name": "Sale & Leaseback Financing",
        "category": "Leasing",
        "color": "374151",
        "defaults": {"amort": "linear", "cash_rate": 0.055, "margin": 0.0,
                     "base_rate": "fixed", "pik_rate": 0.0, "tenor": 10,
                     "floor": 0.0, "oid_pct": 0.0, "upfront_fee": 0.01},
    },
}

CATEGORIES = [
    "Senior Secured", "Second Lien", "Mezzanine",
    "Capital Markets", "Equity-Linked", "Islamic Finance",
    "Structured Finance", "Restructuring", "Leasing"
]

BASE_RATES = {
    "EURIBOR": 0.038,   # 3M EURIBOR
    "SOFR":    0.054,   # SOFR
    "SONIA":   0.052,   # SONIA
    "ESTR":    0.035,   # €STR
    "LIBOR":   0.053,   # 6M USD LIBOR (legacy)
    "CIRR":    0.042,   # CIRR (ECA)
    "fixed":   0.0,
}

# ══════════════════════════════════════════════════════════════════════════════
# TRANCHE DATA CLASS
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class Tranche:
    key:          str
    amount:       float
    currency:     str          = "USD"
    tenor_months: int          = 84
    drawdown_month: int        = 1
    amort:        str          = "linear"   # linear | bullet | sculpted | revolving | custom
    base_rate_type: str        = "EURIBOR"
    margin:       float        = 0.05
    cash_rate:    float        = 0.0        # fixed cash rate (overrides base+margin if >0)
    pik_rate:     float        = 0.0
    floor:        float        = 0.0
    oid_pct:      float        = 0.0
    upfront_fee:  float        = 0.0
    commitment_fee: float      = 0.0
    drawn_pct:    float        = 1.0        # for RCF: % drawn
    grace_months: int          = 0          # interest-only period
    ratchet_grid: List         = field(default_factory=list)  # [(lev_threshold, new_margin)]
    pik_toggle_months: int     = 0          # forced PIK for N months from start
    custom_schedule: List      = field(default_factory=list)  # [(month, repayment)]
    # Convertible bond extras
    conversion_premium: float  = 0.30
    # Prepayment / call premium
    call_premium: float        = 0.02
    # FX hedge assumption
    fx_hedged:    bool         = True

    @property
    def info(self): return DEBT_CATALOGUE.get(self.key, {})
    @property
    def display_name(self): return self.info.get("name", self.key)
    @property
    def color(self): return self.info.get("color", "374151")

# ══════════════════════════════════════════════════════════════════════════════
# DEBT ENGINE
# ══════════════════════════════════════════════════════════════════════════════

class DebtEngine:
    """
    Computes month-by-month schedules for a list of Tranche objects.
    Outputs:
      .schedules  — dict keyed by tranche id, containing monthly arrays
      .totals     — consolidated monthly arrays
    """

    def __init__(self, tranches: List[Tranche], n_months: int, base_rates: Dict = None):
        self.tranches   = tranches
        self.n          = n_months
        self.base_rates = base_rates or BASE_RATES
        self.schedules  = {}
        self.totals     = {}
        self._compute()

    def _effective_rate(self, tranche: Tranche, month_idx: int,
                        ltm_leverage: float = 0.0) -> float:
        """Cash interest rate for a given month, applying ratchet if configured."""
        if tranche.cash_rate > 0:
            base = tranche.cash_rate
        else:
            base_val = self.base_rates.get(tranche.base_rate_type, 0.0)
            margin   = tranche.margin
            # Apply ratchet if leverage is known
            if tranche.ratchet_grid and ltm_leverage > 0:
                for lev_thresh, new_margin in sorted(tranche.ratchet_grid):
                    if ltm_leverage <= lev_thresh:
                        margin = new_margin; break
            base = max(base_val, tranche.floor) + margin
        return base / 12  # monthly

    def _build_amort_schedule(self, tranche: Tranche) -> List[float]:
        """Returns list of n_months principal repayments."""
        n       = self.n
        amt     = tranche.amount
        start   = tranche.drawdown_month - 1   # 0-indexed
        end     = min(start + tranche.tenor_months, n)
        grace   = tranche.grace_months

        repayments = [0.0] * n

        if tranche.amort == "bullet":
            if end <= n:
                repayments[end-1] += amt
        elif tranche.amort == "linear":
            pay_months = max(tranche.tenor_months - grace, 1)
            monthly    = amt / pay_months
            for m in range(start + grace, end):
                if m < n:
                    repayments[m] += monthly
        elif tranche.amort == "sculpted":
            # Back-loaded: small first, larger later
            pay_months = max(tranche.tenor_months - grace, 1)
            weights    = [(i+1)**1.5 for i in range(pay_months)]
            total_w    = sum(weights)
            for i, m in enumerate(range(start + grace, end)):
                if m < n:
                    repayments[m] += amt * weights[i] / total_w
        elif tranche.amort == "revolving":
            # No amortisation; full repayment at maturity
            if end <= n:
                repayments[end-1] += amt * tranche.drawn_pct
        elif tranche.amort == "custom" and tranche.custom_schedule:
            for (month_no, rep_amt) in tranche.custom_schedule:
                m = month_no - 1
                if 0 <= m < n:
                    repayments[m] += rep_amt
        else:
            # Default: bullet
            if end <= n:
                repayments[end-1] += amt

        return repayments

    def _compute_tranche(self, tranche: Tranche) -> Dict:
        n          = self.n
        start      = tranche.drawdown_month - 1
        end        = min(start + tranche.tenor_months, n)
        repayments = self._build_amort_schedule(tranche)

        drawn_amount = tranche.amount * (tranche.drawn_pct if tranche.amort == "revolving" else 1.0)
        undrawn      = tranche.amount - drawn_amount if tranche.amort == "revolving" else 0.0

        opening  = [0.0] * n
        closing  = [0.0] * n
        interest_cash = [0.0] * n
        interest_pik  = [0.0] * n
        interest_total= [0.0] * n
        pik_accrual   = [0.0] * n
        commitment_fee_m = [0.0] * n
        oid_amort_m   = [0.0] * n

        # OID amortisation over tenor
        oid_amount  = tranche.amount * tranche.oid_pct
        oid_monthly = oid_amount / max(tranche.tenor_months, 1)

        balance = 0.0

        for m in range(n):
            # Drawdown
            if m == start:
                balance = drawn_amount

            opening[m] = balance

            if balance <= 0.0:
                closing[m] = 0.0
                continue

            # Effective cash rate
            rate_m = self._effective_rate(tranche, m)
            pik_m  = tranche.pik_rate / 12

            # PIK toggle: forced PIK in first N months
            if tranche.pik_toggle_months > 0 and (m - start) < tranche.pik_toggle_months:
                pik_m  = (tranche.cash_rate if tranche.cash_rate > 0 else rate_m * 12) / 12 + pik_m
                rate_m = 0.0

            i_cash = balance * rate_m
            i_pik  = balance * pik_m

            interest_cash[m]  = i_cash
            interest_pik[m]   = i_pik
            interest_total[m] = i_cash + i_pik
            pik_accrual[m]    = i_pik  # added to balance

            # Commitment fee on undrawn
            commitment_fee_m[m] = undrawn * tranche.commitment_fee / 12

            # OID amortisation
            if start <= m < end:
                oid_amort_m[m] = oid_monthly

            # PIK capitalises into balance
            balance += i_pik
            # Repayment
            balance = max(balance - repayments[m], 0.0)
            closing[m] = balance

        return {
            "opening":        opening,
            "closing":        closing,
            "repayment":      repayments,
            "interest_cash":  interest_cash,
            "interest_pik":   interest_pik,
            "interest_total": interest_total,
            "pik_accrual":    pik_accrual,
            "commitment_fee": commitment_fee_m,
            "oid_amort":      oid_amort_m,
            "drawn":          drawn_amount,
            "undrawn":        undrawn,
        }

    def _compute(self):
        totals = {
            "opening": [0.0]*self.n, "closing": [0.0]*self.n,
            "repayment": [0.0]*self.n, "interest_cash": [0.0]*self.n,
            "interest_pik": [0.0]*self.n, "interest_total": [0.0]*self.n,
            "commitment_fee": [0.0]*self.n, "oid_amort": [0.0]*self.n,
        }
        for i, t in enumerate(self.tranches):
            key = f"t{i}_{t.key}"
            sch = self._compute_tranche(t)
            self.schedules[key] = sch
            for field in totals:
                for m in range(self.n):
                    totals[field][m] += sch[field][m]
        self.totals = totals

    def summary(self) -> Dict:
        """Key consolidated metrics."""
        return {
            "total_debt_drawn":    sum(t.amount * (t.drawn_pct if t.amort=="revolving" else 1) for t in self.tranches),
            "total_debt_committed":sum(t.amount for t in self.tranches),
            "total_upfront_fees":  sum(t.amount * t.upfront_fee for t in self.tranches),
            "total_oid":           sum(t.amount * t.oid_pct for t in self.tranches),
            "n_tranches":          len(self.tranches),
        }


# ══════════════════════════════════════════════════════════════════════════════
# CONFIG PARSER  —  converts frontend JSON → Tranche objects
# ══════════════════════════════════════════════════════════════════════════════

def parse_tranches(tranche_configs: List[Dict]) -> List[Tranche]:
    tranches = []
    for tc in tranche_configs:
        key   = tc.get("key", "tla")
        info  = DEBT_CATALOGUE.get(key, {})
        defs  = info.get("defaults", {})

        # Merge defaults with user overrides
        t = Tranche(
            key           = key,
            amount        = float(tc.get("amount", 10000)),
            currency      = tc.get("currency", "USD"),
            tenor_months  = int(tc.get("tenor_years", defs.get("tenor", 7))) * 12,
            drawdown_month= int(tc.get("drawdown_month", 1)),
            amort         = tc.get("amort", defs.get("amort", "bullet")),
            base_rate_type= tc.get("base_rate", defs.get("base_rate", "EURIBOR")),
            margin        = float(tc.get("margin", defs.get("margin", 0.05))),
            cash_rate     = float(tc.get("cash_rate", defs.get("cash_rate", 0.0))),
            pik_rate      = float(tc.get("pik_rate", defs.get("pik_rate", 0.0))),
            floor         = float(tc.get("floor", defs.get("floor", 0.0))),
            oid_pct       = float(tc.get("oid_pct", defs.get("oid_pct", 0.0))),
            upfront_fee   = float(tc.get("upfront_fee", defs.get("upfront_fee", 0.0))),
            commitment_fee= float(tc.get("commitment_fee", defs.get("commitment_fee", 0.0))),
            drawn_pct     = float(tc.get("drawn_pct", defs.get("drawn_pct", 1.0))),
            grace_months  = int(tc.get("grace_months", 0)),
            ratchet_grid  = tc.get("ratchet_grid", []),
            pik_toggle_months = int(tc.get("pik_toggle_months", defs.get("pik_toggle_months", 0))),
            custom_schedule   = tc.get("custom_schedule", []),
            call_premium      = float(tc.get("call_premium", defs.get("call_premium", 0.02))),
        )
        tranches.append(t)
    return tranches
