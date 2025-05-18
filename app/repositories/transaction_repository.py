from app.services.data_service import read_data

class TransactionRepository:
    def get_all_transactions(self):
        return read_data().get("transactions", [])

def get_transaction_repository():
    return TransactionRepository()