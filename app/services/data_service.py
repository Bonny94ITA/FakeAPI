# app/services/data_service.py
import json
from pathlib import Path
from typing import List, Dict

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "data.json"

def read_data() -> Dict[str, List[Dict]]:
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def write_data(data: Dict[str, List[Dict]]) -> None:
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_user(user: Dict) -> None:
    data = read_data()
    data["users"].append(user)
    write_data(data)
