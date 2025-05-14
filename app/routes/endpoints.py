# app/routes/endpoints.py
from fastapi import APIRouter
from typing import List
from app.models.schemas import User, Transaction, Campaign
from app.services.data_service import read_data, add_user

router = APIRouter()

@router.get("/users", response_model=List[User])
def get_users():
    return read_data().get("users", [])

@router.get("/transactions", response_model=List[Transaction])
def get_transactions():
    return read_data().get("transactions", [])

@router.get("/campaigns", response_model=List[Campaign])
def get_campaigns():
    return read_data().get("campaigns", [])

@router.post("/user", status_code=201)
def create_user(user: User):
    add_user(user.dict())
    return {"message": "User added successfully"}
