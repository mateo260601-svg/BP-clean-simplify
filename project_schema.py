from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from datetime import datetime

class UploadedDocument(BaseModel):
    file_id: str
    filename: str
    path: str
    category: str = "financials"
    uploaded_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ProjectRecord(BaseModel):
    project_id: str
    name: str
    company_name: str = "Target Company"
    sector: str = "General"
    currency: str = "EUR"
    deal_type: str = "M&A"
    status: str = "Active"
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    license_key: str
    documents: List[UploadedDocument] = Field(default_factory=list)
    intake: Dict[str, Any] = Field(default_factory=dict)
    extracted_financials: Optional[Dict[str, Any]] = None
    outputs: Dict[str, str] = Field(default_factory=dict)
    module_status: Dict[str, str] = Field(default_factory=lambda: {
        "bp": "Not started",
        "deck": "Not started",
        "qoe": "Not started",
        "restructuring": "Not started",
    })
    notes: str = ""
