from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date

class UserCreate(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Alice"})
    email: Optional[EmailStr] = Field(..., json_schema_extra={"example": "alice@example.com"})
    city: str = Field(..., json_schema_extra={"example": "Milan"})

class User(UserCreate):
    id: int

class Transaction(BaseModel):
    id: int
    user_id: int
    campaign_id: int
    amount: float = Field(..., json_schema_extra={"example": 99.99})
    date: str = Field(..., json_schema_extra={"example": "2025-01-01"})

class Campaign(BaseModel):
    id: int
    name: str = Field(..., json_schema_extra={"example": "Summer Sale"})
    channel: str = Field(..., json_schema_extra={"example": "Email"})
    budget: float = Field(..., json_schema_extra={"example": 10000.00})
    start_date: date = Field(..., json_schema_extra={"example": "2025-05-01"})
    end_date: date = Field(..., json_schema_extra={"example": "2025-06-01"})
