import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.models.schemas import User, Transaction, Campaign
from pydantic import ValidationError
import json

DATA_FILE = Path("app/data/data.json")

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def test_validate_users():
    raw_data = load_data()
    errors = []
    for i, item in enumerate(raw_data.get("users", []), 1):
        try:
            User(**item)
        except ValidationError as e:
            errors.append(f"User #{i} invalid: {e}")
    assert not errors, "\n".join(errors)

def test_validate_transactions():
    raw_data = load_data()
    errors = []
    for i, item in enumerate(raw_data.get("transactions", []), 1):
        try:
            Transaction(**item)
        except ValidationError as e:
            errors.append(f"Transaction #{i} invalid: {e}")
    assert not errors, "\n".join(errors)

def test_validate_campaigns():
    raw_data = load_data()
    errors = []
    for i, item in enumerate(raw_data.get("campaigns", []), 1):
        try:
            Campaign(**item)
        except ValidationError as e:
            errors.append(f"Campaign #{i} invalid: {e}")
    assert not errors, "\n".join(errors)