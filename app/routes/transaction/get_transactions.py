from fastapi import APIRouter
from typing import List
from app.models.transaction import Transaction
from app.repositories.transaction_repository import TransactionRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

get_tran = APIRouter()
transaction_repository = TransactionRepository()

@get_tran.get("/transactions", response_model=List[Transaction])
def get_transactions():
    logger.info("GET /transactions called")
    return transaction_repository.get_all_transactions()




