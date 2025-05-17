from fastapi import APIRouter, HTTPException
from app.schemas.user import User
from app.schemas.user_create import UserCreate
from app.repositories.user_repository import UserRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

post_usr = APIRouter()
user_repository = UserRepository()

@post_usr.post("/user", status_code=201, response_model=User)
def create_user(user: UserCreate):
    try:
        new_user = user_repository.add_user(user.model_dump())
    except Exception as e:
        logger.error(f"Error adding user: {getattr(e, 'details', str(e))}", exc_info=True)
        if "Email" in str(e):
            raise HTTPException(status_code=400, detail="Email already exists")
        else:
            raise HTTPException(status_code=500, detail="Error saving user")
    logger.info(f"User added successfully: {new_user}")
    return new_user

