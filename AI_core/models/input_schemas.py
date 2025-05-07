"""
Pydantic models for input validation.
"""
from pydantic import BaseModel, Field

class ReportGenerationInput(BaseModel):
    """Input schema for the report generation tool."""
    case_name: str = Field(description="Name of the legal case")
    case_facts: str = Field(description="Key facts of the case")
    legal_issues: str = Field(description="Legal issues identified in the case")
    applicable_laws: str = Field(description="Laws and regulations applicable to this case")