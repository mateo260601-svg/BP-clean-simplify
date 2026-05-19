"""deck_generator.py — end-to-end IM deck generation helper."""
from __future__ import annotations
from typing import Dict, Any, Optional
from pathlib import Path
from financial_normalizer import normalise_from_extractor_payload, model_from_bp_config
from template_selector import included_slides, select_slides
from pptx_builder import build_im_deck

def generate_im_deck_from_payload(payload: Dict[str, Any], output_path: str, template_path: Optional[str]=None) -> Dict[str, Any]:
    model = normalise_from_extractor_payload(payload or {})
    slides = included_slides(model)
    build_im_deck(model, slides, output_path, template_path=template_path)
    return {"success": True, "output_path": output_path, "company_name": model.get("company_name"), "slides_included": [s["id"] for s in slides], "slide_selection": select_slides(model), "data_quality": model.get("checks",{}).get("quality_label"), "checks": model.get("checks")}

def generate_im_deck_from_config(config: Dict[str, Any], output_path: str, template_path: Optional[str]=None) -> Dict[str, Any]:
    model = model_from_bp_config(config or {})
    slides = included_slides(model)
    build_im_deck(model, slides, output_path, template_path=template_path)
    return {"success": True, "output_path": output_path, "company_name": model.get("company_name"), "slides_included": [s["id"] for s in slides], "slide_selection": select_slides(model), "data_quality": model.get("checks",{}).get("quality_label"), "checks": model.get("checks")}
