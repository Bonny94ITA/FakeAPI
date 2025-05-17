from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Alice"})
    email: Optional[EmailStr] = Field(..., json_schema_extra={"example": "alice@example.com"})
    city: str = Field(..., json_schema_extra={"example": "Milan"})
