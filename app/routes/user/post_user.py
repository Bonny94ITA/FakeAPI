from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import User
from app.schemas.user_create import UserCreate
from app.repositories.user_repository import get_user_repository, UserRepository
from app.services.data_service import DuplicateEmailException
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

post_usr = APIRouter()

@post_usr.post("/user", status_code=201, response_model=User)
def create_user(
    user: UserCreate,
    user_repository: UserRepository = Depends(get_user_repository)
):
    try:
        new_user = user_repository.add_user(user.model_dump())
    except DuplicateEmailException:
        logger.warning("Duplicate email")
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error saving user")
    logger.info(f"User added successfully: {new_user}")
    return new_user

