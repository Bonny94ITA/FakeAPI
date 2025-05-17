from pathlib import Path
from typing import List, Dict
from filelock import FileLock
import json

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "data.json"
LOCK_FILE = DATA_FILE.with_suffix(".lock")

def read_data() -> Dict[str, List[Dict]]:
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def _is_duplicate_email(email: str, users: List[Dict]) -> bool:
    if not email:
        return False
    email = email.lower()
    return any(
        u.get("email") and u["email"].lower() == email
        for u in users
    )

def add_user(user_partial: Dict) -> Dict:
    with FileLock(str(LOCK_FILE)):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        users = data.get("users", [])

        email = user_partial.get("email")
        if _is_duplicate_email(email, users):
            raise ValueError("Email already exists")

        last_id = max((u["id"] for u in users), default=0)
        new_user = {"id": last_id + 1, **user_partial}

        users.append(new_user)
        data["users"] = users

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    return new_user

