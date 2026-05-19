from financial_schema import NormalizedFinancials
from template_selector import select_im_sections
from pptx_builder import build_im_deck

def generate_deck(financials: NormalizedFinancials, output_path: str) -> str:
    sections = select_im_sections(financials)
    return build_im_deck(financials, sections, output_path)
