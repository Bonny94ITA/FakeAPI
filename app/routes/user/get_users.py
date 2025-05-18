from fastapi import APIRouter, Depends
from typing import List
from app.schemas.user import User
from app.repositories.user_repository import get_user_repository, UserRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

get_usr = APIRouter()

@get_usr.get("/users", response_model=List[User])
def get_users(
    user_repository: UserRepository = Depends(get_user_repository)
):
    logger.info("GET /users called")
    return user_repository.get_all_users()