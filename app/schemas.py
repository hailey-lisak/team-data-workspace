# app/schemas.py
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator


class RecordIngestRow(BaseModel):
    """Schema representing a single parsed row from the CSV file."""

    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(..., min_length=1, description="Contact full name")
    email: str = Field(..., min_length=1, description="Contact email address")
    company: Optional[str] = Field(None, description="Company name")
    city: Optional[str] = Field(None, description="City location")
    notes: Optional[str] = Field(None, description="Additional notes")

    @field_validator("company", "city", "notes", mode="before")
    @classmethod
    def empty_string_to_none(cls, v: Any) -> Optional[str]:
        """Convert empty or whitespace-only strings to None (SQL NULL)."""
        if isinstance(v, str):
            v = v.strip()
            return v if v else None
        return v


class CSVValidationResult(BaseModel):
    """Schema for the overall parsing response."""

    valid_count: int
    error_count: int
    valid_records: List[RecordIngestRow]
    errors: List[Dict[str, Any]]