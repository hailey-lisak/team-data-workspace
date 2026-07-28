import requests

BASE_URL = "http://localhost:8000"

def test_jobs_api():
    print("\n=== STARTING INTEGRATION TEST: JOBS (POST, GET, PUT) ===")

    # 1. POST (Create)
    job_payload = {"job_type": "csv_export", "status": "pending"}
    print("1. Calling POST /jobs/ to create background task...")
    create_resp = requests.post(f"{BASE_URL}/jobs/", json=job_payload)
    assert create_resp.status_code in (200, 201), f"Create failed: {create_resp.text}"
    job_id = create_resp.json()["id"]
    print(f"  -> SUCCESS: Created Job ID {job_id}")

    # 2. GET (Read)
    print(f"2. Calling GET /jobs/{job_id}")
    get_resp = requests.get(f"{BASE_URL}/jobs/{job_id}")
    assert get_resp.status_code == 200, f"Read failed: {get_resp.text}"
    print(f"  -> SUCCESS: Job status is '{get_resp.json().get('status')}'")

    # 3. PUT (Full Replace / Update)
    put_payload = {"job_type": "csv_export", "status": "completed"}
    print(f"3. Calling PUT /jobs/{job_id} to replace resource state...")
    put_resp = requests.put(f"{BASE_URL}/jobs/{job_id}", json=put_payload)
    assert put_resp.status_code == 200, f"PUT update failed: {put_resp.text}"
    print(f"  -> SUCCESS: Job status updated via PUT to '{put_resp.json().get('status')}'")

    # Negative Test
    print("\n--- Testing Corrupted Endpoint (Negative Test) ---")
    try:
        bad_resp = requests.get(f"{BASE_URL}/jobs_invalid_route/{job_id}")
        bad_resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"  -> EXPECTED ERROR CAUGHT! Status {bad_resp.status_code}: {err}")

    print("=== JOBS INTEGRATION TEST COMPLETED ===\n")

if __name__ == "__main__":
    test_jobs_api()