from fastapi import APIRouter
from typing import List
from app.schemas.user import User
from app.repositories.user_repository import UserRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

get_usr = APIRouter()
user_repository = UserRepository()

@get_usr.get("/users", response_model=List[User])
def get_users():
    logger.info("GET /users called")
    return user_repository.get_all_users()
