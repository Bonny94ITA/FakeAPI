from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import pytest
import requests

def call_generate_reports(n):
    response = requests.post("http://127.0.0.1:8000/generate_reports")
    return n, response.status_code, response.json()

@pytest.mark.parametrize("num_requests", [5])
def test_concurrent_report_generation(num_requests):
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(call_generate_reports, i) for i in range(num_requests)]
        for future in as_completed(futures):
            n, status, data = future.result()
            assert status == 200, f"Report generation {n} failed: {data}"