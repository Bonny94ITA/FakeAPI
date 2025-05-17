from app.services.data_service import read_data, add_user

class UserRepository:
    def get_all_users(self):
        return read_data().get("users", [])

    def add_user(self, user_data):
        return add_user(user_data)