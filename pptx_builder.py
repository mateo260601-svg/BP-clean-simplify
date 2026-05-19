from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from financial_schema import NormalizedFinancials

NAVY = RGBColor(6, 26, 58)
BLUE = RGBColor(11, 95, 255)
GREY = RGBColor(100, 116, 139)

def _add_title(slide, title, subtitle=None):
    tx = slide.shapes.add_textbox(Inches(0.55), Inches(0.35), Inches(12.1), Inches(0.7))
    tx.text_frame.text = title
    p = tx.text_frame.paragraphs[0]
    p.font.size = Pt(26); p.font.bold = True; p.font.color.rgb = NAVY
    if subtitle:
        st = slide.shapes.add_textbox(Inches(0.58), Inches(1.02), Inches(11.8), Inches(0.35))
        st.text_frame.text = subtitle
        st.text_frame.paragraphs[0].font.size = Pt(11)
        st.text_frame.paragraphs[0].font.color.rgb = GREY

def _footer(slide, page):
    box = slide.shapes.add_textbox(Inches(0.55), Inches(7.05), Inches(12), Inches(0.25))
    box.text_frame.text = f"Private & Confidential | MG Advisory | {page}"
    box.text_frame.paragraphs[0].font.size = Pt(8)
    box.text_frame.paragraphs[0].font.color.rgb = GREY

def _metric_card(slide, x, y, label, value):
    shape = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(2.55), Inches(1.0))
    shape.fill.solid(); shape.fill.fore_color.rgb = RGBColor(245, 248, 252)
    shape.line.color.rgb = RGBColor(226, 232, 240)
    t = slide.shapes.add_textbox(Inches(x+0.15), Inches(y+0.15), Inches(2.2), Inches(0.25))
    t.text_frame.text = label
    t.text_frame.paragraphs[0].font.size = Pt(9); t.text_frame.paragraphs[0].font.color.rgb = GREY
    v = slide.shapes.add_textbox(Inches(x+0.15), Inches(y+0.48), Inches(2.2), Inches(0.35))
    v.text_frame.text = value
    v.text_frame.paragraphs[0].font.size = Pt(18); v.text_frame.paragraphs[0].font.bold = True
    v.text_frame.paragraphs[0].font.color.rgb = NAVY

def build_im_deck(financials: NormalizedFinancials, sections, output_path: str) -> str:
    prs = Presentation()
    prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid(); slide.background.fill.fore_color.rgb = RGBColor(248, 250, 252)
    title = slide.shapes.add_textbox(Inches(0.75), Inches(1.3), Inches(8.5), Inches(1.4))
    title.text_frame.text = financials.company_name
    title.text_frame.paragraphs[0].font.size = Pt(44); title.text_frame.paragraphs[0].font.bold = True
    title.text_frame.paragraphs[0].font.color.rgb = NAVY
    sub = slide.shapes.add_textbox(Inches(0.8), Inches(2.65), Inches(8), Inches(0.6))
    sub.text_frame.text = "Investment Memorandum | Confidential"
    sub.text_frame.paragraphs[0].font.size = Pt(20); sub.text_frame.paragraphs[0].font.color.rgb = BLUE
    _footer(slide, 1)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_title(slide, "Investment Highlights", "Automatically generated from uploaded financial materials")
    latest = financials.periods[-1] if financials.periods else None
    _metric_card(slide, 0.7, 1.55, "Revenue", f"{financials.currency} {latest.revenue:,.1f}" if latest and latest.revenue else "N/A")
    _metric_card(slide, 3.55, 1.55, "EBITDA", f"{financials.currency} {latest.ebitda:,.1f}" if latest and latest.ebitda else "N/A")
    _metric_card(slide, 6.4, 1.55, "Cash", f"{financials.currency} {latest.cash:,.1f}" if latest and latest.cash else "N/A")
    _metric_card(slide, 9.25, 1.55, "Debt", f"{financials.currency} {latest.debt:,.1f}" if latest and latest.debt else "N/A")
    box = slide.shapes.add_textbox(Inches(0.85), Inches(3.05), Inches(11.5), Inches(2.5))
    tf = box.text_frame; tf.clear()
    for b in ["Strategic platform with institutional reporting now standardised", "Financials extracted and normalised into a banking-ready data model", "Further diligence required for quality check flags"]:
        p = tf.add_paragraph(); p.text = b; p.font.size = Pt(17); p.font.color.rgb = NAVY
    _footer(slide, 2)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_title(slide, "Financial Overview", "Historical financials normalised from source documents")
    rows = len(financials.periods) + 1
    table = slide.shapes.add_table(rows, 5, Inches(0.7), Inches(1.55), Inches(11.9), Inches(3.4)).table
    headers = ["Period", "Revenue", "EBITDA", "Cash", "Debt"]
    for c, h in enumerate(headers): table.cell(0, c).text = h
    for r, p in enumerate(financials.periods, start=1):
        for c, val in enumerate([p.period, p.revenue, p.ebitda, p.cash, p.debt]):
            table.cell(r, c).text = f"{val:,.1f}" if isinstance(val, (int, float)) else str(val or "")
    _footer(slide, 3)

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _add_title(slide, "Process & Next Steps", "Recommended diligence steps")
    for i, s in enumerate(["Validate extracted figures", "Confirm QoE adjustments", "Populate customer / market sections", "Finalise IM and investor process"]):
        _metric_card(slide, 0.8 + (i % 2)*5.8, 1.6 + (i//2)*1.5, f"Step {i+1}", s)
    _footer(slide, 4)

    prs.save(output_path)
    return output_path
