from fastapi import APIRouter, Depends
from typing import List
from app.schemas.transaction import Transaction
from app.repositories.transaction_repository import get_transaction_repository, TransactionRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

get_tran = APIRouter()

@get_tran.get("/transactions", response_model=List[Transaction])
def get_transactions(
    transaction_repository: TransactionRepository = Depends(get_transaction_repository)
):
    logger.info("GET /transactions called")
    return transaction_repository.get_all_transactions()




