from fastapi import APIRouter, HTTPException
from app.models.user_create import UserCreate
from app.repositories.user_repository import UserRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

post_usr = APIRouter()
user_repository = UserRepository()

@post_usr.post("/user", status_code=201)
def create_user(user: UserCreate):
    try:
        new_user = user_repository.add_user(user.model_dump())
    except Exception as e:
        logger.error(f"Error adding user: {e}")
        if "Email" in str(e):
            raise HTTPException(status_code=400, detail="Email already exists")
        else:
            raise HTTPException(status_code=500, detail="Error saving user")

    logger.info(f"User added successfully: {new_user}")
    return {"message": "User added successfully", "user": new_user}

