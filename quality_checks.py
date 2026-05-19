from financial_schema import NormalizedFinancials

def run_quality_checks(financials: NormalizedFinancials):
    flags = list(financials.quality_flags)
    for p in financials.periods:
        if p.revenue and p.ebitda and abs(p.ebitda) > abs(p.revenue):
            flags.append(f"{p.period}: EBITDA greater than revenue")
        if p.debt and p.ebitda and p.ebitda > 0 and p.debt / p.ebitda > 8:
            flags.append(f"{p.period}: high leverage above 8.0x")
    financials.quality_flags = sorted(set(flags))
    return financials
