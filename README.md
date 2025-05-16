# FakeAPI

A local API built with FastAPI that serves data from a JSON file and provides endpoints for users, transactions, and campaigns.  
Includes a data processing pipeline for generating analytical CSV reports, with robust concurrency and validation testing.

---

## Features

- **FastAPI** backend with endpoints for users, transactions, and campaigns
- **Data persistence** via `app/data/data.json`
- **POST /user** endpoint to add new users
- **/generate_reports** endpoint: fetches, cleans, aggregates, and exports data as CSV reports
- **Concurrency-safe** CSV writing using `filelock`
- **Automated validation** and concurrency tests with `pytest`

---

## Requirements

- Python 3.9+
- See `requirements.txt` for dependencies

---

## Setup

1. **Clone the repository**
   ```sh
   git clone <your-repo-url>
   cd FakeAPI
   ```

2. **Create a virtual environment (recommended)**
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

---

## Running the API

Start the FastAPI server with:

```sh
uvicorn app.main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Docker

You can run the API in a container using the provided `Dockerfile`.

### Build the Docker image

```sh
docker build -t fakeapi .
```

### Run the Docker container

```sh
docker run -p 8000:8000 fakeapi
```

The API will be available at [http://localhost:8000](http://localhost:8000).

> **Note:**  
> The container will use the `app/data/data.json` file inside the container.  
> If you want to persist or edit data outside the container, you can mount a volume:

```sh
docker run -p 8000:8000 -v $(pwd)/app/data:/app/app/data fakeapi
```

---

## API Endpoints

- `GET /users` — Fetch all users
- `GET /transactions` — Fetch all transactions
- `GET /campaigns` — Fetch all campaigns
- `POST /user` — Add a new user (JSON body: `name`, `email`, `city`)
- `POST /generate_reports` — Run the full data pipeline and generate CSV reports in the `reports/` folder

---

## Reports

After calling `POST /generate_reports`, you will find:

- `reports/user_campaign_report.csv`
- `reports/campaign_revenue_report.csv`

---

## Testing

### Run all tests

```sh
pytest
```

### Test concurrent user creation

```sh
pytest test_concurrent_post.py
```

### Test concurrent report generation

```sh
pytest test_concurrent_reports.py
```

### Validate data schemas

```sh
pytest tests/test_validate_data.py
```

---

## Notes

- The API is concurrency-safe for file writes thanks to `filelock`.
- Data validation is enforced via Pydantic models.
- For development, you can reset or edit `app/data/data.json` as needed.
- If you add new dependencies, update `requirements.txt` and reinstall.

---

## Troubleshooting

- **ModuleNotFoundError: No module named 'app'**  
  Make sure to run `pytest` from the project root (`FakeAPI/`), not from inside the `tests/` folder.
- **Email validation errors**  
  Ensure `email-validator` is installed (`pip install email-validator`).

---

## Project Structure

```
FakeAPI/
│
├── app/
│   ├── data/
│   │   └── data.json
│   ├── models/
│   │   └── schemas.py
│   ├── routes/
│   │   ├── endpoints.py
│   │   └── reports.py
│   ├── services/
│   │   └── data_service.py
│   └── main.py
│
├── reports/
│   ├── user_campaign_report.csv
│   └── campaign_revenue_report.csv
│
├── tests/
│   └── test_validate_data.py
│
├── test_concurrent_post.py
├── test_concurrent_reports.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## License

MIT License

---

## Author

Giacomo
