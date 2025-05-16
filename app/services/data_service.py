from pathlib import Path
from typing import List, Dict
from filelock import FileLock
import json

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "data.json"
LOCK_FILE = DATA_FILE.with_suffix(".lock")

def read_data() -> Dict[str, List[Dict]]:
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def add_user(user_partial: Dict) -> Dict:
    with FileLock(str(LOCK_FILE)):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)

        users = data.get("users", [])

        if user_partial.get("email"):
            if any(
                u.get("email") and u["email"].lower() == user_partial["email"].lower()
                for u in users
            ):
                raise ValueError("Email already exists")

        last_id = max((u["id"] for u in users), default=0)
        new_user = {"id": last_id + 1, **user_partial}

        users.append(new_user)
        data["users"] = users

        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)

    return new_user

