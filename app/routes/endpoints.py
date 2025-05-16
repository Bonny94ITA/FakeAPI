from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import UserCreate, User, Transaction, Campaign
from app.services.data_service import read_data, add_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
def create_user(user: UserCreate):
    try:
        new_user = add_user(user.model_dump())
    except Exception as e:
        logger.error(f"Error adding user: {e}")
        raise HTTPException(status_code=400, detail="Email already exists") if "Email" in str(e) else HTTPException(status_code=500, detail="Error saving user")

    logger.info(f"User added successfully: {new_user}")
    return {"message": "User added successfully", "user": new_user}

