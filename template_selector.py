from financial_schema import NormalizedFinancials

def select_im_sections(financials: NormalizedFinancials):
    sections = ["cover", "disclaimer", "contents", "investment_highlights"]
    if any(p.revenue or p.ebitda for p in financials.periods):
        sections.append("financial_overview")
    if any(p.debt for p in financials.periods):
        sections.append("capital_structure")
    sections.extend(["value_creation", "process_next_steps"])
    return sections
