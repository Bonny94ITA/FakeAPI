# FakeAPI

FakeAPI is a simple FastAPI project that manages users, transactions, and campaigns, storing everything in a JSON file.  
It also includes a pipeline to generate CSV reports, concurrency-safe file handling, and both unit and integration tests.

This project uses some classic design patterns to keep the code clean and maintainable, such as the **Repository Pattern** (for data access) and the **Template Method Pattern** (for the reporting pipeline).

---

## Features

- REST API for users, transactions, and campaigns
- Data stored in `app/data/data.json`
- Add users via `POST /user`
- Generate analytical CSV reports with `/generate_reports`
- Concurrency-safe file writes (using filelock)
- Automated tests (unit and integration)
- Clean architecture with Repository and Template Method patterns

---

## Quickstart

### 1. Install

```sh
git clone https://github.com/Bonny94ITA/FakeAPI
cd FakeAPI
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the API

```sh
uvicorn app.main:app --reload
```
Swagger UI Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 3. Docker (optional)

Build the image:
```sh
docker build -t fake-api .
```
Run the container:
```sh
docker run -p 8000:8000 fake-api
```
To persist data outside the container:
```sh
docker run -p 8000:8000 -v $(pwd)/app/data:/app/app/data fakeapi
```

---

## Main Endpoints

- `GET /users` — List users
- `POST /user` — Add a user
- `GET /transactions` — List transactions
- `GET /campaigns` — List campaigns
- `POST /generate_reports` — Generate CSV reports

---

## Reports

After calling `/generate_reports` you’ll find:
- `reports/user_campaign_report.csv`
- `reports/campaign_revenue_report.csv`

---

## Testing

Run all tests:
```sh
pytest
```
Integration tests for concurrency:
```sh
pytest tests/integration/test_concurrent_post.py
pytest tests/integration/test_concurrent_reports.py
```

---

## Notes

- File writes are concurrency-safe thanks to filelock.
- Data validation is handled by Pydantic.
- The codebase uses the Repository and Template Method patterns for clarity and extensibility.
- **Note:** The `email` field for users accepts `null` values, but if an email is provided and it is not valid, the API will return a validation error.

---

## Author

Giacomo

---
