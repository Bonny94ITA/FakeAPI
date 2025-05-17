from concurrent.futures import ThreadPoolExecutor, as_completed
import pytest
import requests
import uuid
import shutil
import os

DATA_FILE = "app/data/data.json"
TEST_DATA_FILE = "app/data/data_test.json"

@pytest.fixture(autouse=True)
def isolate_data_file():
    # Backup original file
    if os.path.exists(DATA_FILE):
        shutil.copy(DATA_FILE, DATA_FILE + ".bak")
    # Replace with test data
    if os.path.exists(TEST_DATA_FILE):
        shutil.copy(TEST_DATA_FILE, DATA_FILE)
    yield
    # Restore original file after test
    if os.path.exists(DATA_FILE + ".bak"):
        shutil.move(DATA_FILE + ".bak", DATA_FILE)

def post_user(n):
    unique_email = f"user{n}_{uuid.uuid4().hex}@example.com"
    response = requests.post("http://127.0.0.1:8000/user", json={
        "name": f"User{n}",
        "email": unique_email,
        "city": "TestCity"
    })
    return n, response.status_code, response.json()

@pytest.mark.parametrize("num_users", [10])
def test_concurrent_user_creation(num_users):
    with ThreadPoolExecutor(max_workers=num_users) as executor:
        futures = [executor.submit(post_user, i) for i in range(num_users)]
        for future in as_completed(futures):
            n, status, data = future.result()
            assert status == 201, f"User {n} creation failed: {data}"