from pydantic import BaseModel, Field

class Transaction(BaseModel):
    id: int
    user_id: int
    campaign_id: int
    amount: float = Field(..., json_schema_extra={"example": 99.99})
    date: str = Field(..., json_schema_extra={"example": "2025-01-01"})
