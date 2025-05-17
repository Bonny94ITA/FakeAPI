from pydantic import BaseModel, Field
from datetime import date

class Campaign(BaseModel):
    id: int
    name: str = Field(..., json_schema_extra={"example": "Summer Sale"})
    channel: str = Field(..., json_schema_extra={"example": "Email"})
    budget: float = Field(..., json_schema_extra={"example": 10000.00})
    start_date: date = Field(..., json_schema_extra={"example": "2025-05-01"})
    end_date: date = Field(..., json_schema_extra={"example": "2025-06-01"})
