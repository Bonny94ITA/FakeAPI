# app/models/schemas.py
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    name: str
    email: str

class Transaction(BaseModel):
    id: int
    user_id: int
    amount: float

class Campaign(BaseModel):
    id: int
    name: str
    budget: float
