from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any

class PeriodFinancials(BaseModel):
    period: str
    revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    ebitda: Optional[float] = None
    ebit: Optional[float] = None
    net_income: Optional[float] = None
    cash: Optional[float] = None
    debt: Optional[float] = None
    working_capital: Optional[float] = None
    capex: Optional[float] = None
    free_cash_flow: Optional[float] = None

class NormalizedFinancials(BaseModel):
    company_name: str = "Target Company"
    currency: str = "EUR"
    source_type: str = "unknown"
    periods: List[PeriodFinancials] = Field(default_factory=list)
    raw_text_preview: Optional[str] = None
    raw_tables: List[Dict[str, Any]] = Field(default_factory=list)
    quality_flags: List[str] = Field(default_factory=list)
