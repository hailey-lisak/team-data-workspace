import csv
import os
import requests

BASE_URL = "http://localhost:8000"
WORKSPACE_ID = "workspace-prod-1"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.abspath(os.path.join(CURRENT_DIR, "..", "sample_import.csv"))

def test_records_api():
    print("\n=== STARTING INTEGRATION TEST: RECORDS (POST, GET, DELETE) ===")

    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        return

    created_ids = []

    # 1. POST (CSV Import)
    print("\n--- 1. Testing POST (CSV Streaming) ---")
    with open(CSV_PATH, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader, start=1):
            if not any(val and val.strip() for val in row.values()):
                print(f"[Line {i}] Skipped blank/whitespace row.")
                continue

            payload = {
                "workspace_id": WORKSPACE_ID,
                "name": row.get("name", "").strip(),
                "email": row.get("email", "").strip(),
                "company": row.get("company", "").strip(),
                "city": row.get("city", "").strip(),
                "notes": row.get("notes", "").strip()
            }

            resp = requests.post(f"{BASE_URL}/records/", json=payload)
            if resp.status_code in (200, 201):
                rec_id = resp.json().get("id")
                created_ids.append(rec_id)
                print(f"[Line {i}] Saved record ID: {rec_id}")

    # 2. GET (Read)
    print("\n--- 2. Testing GET ---")
    get_resp = requests.get(f"{BASE_URL}/records/?workspace_id={WORKSPACE_ID}")
    assert get_resp.status_code == 200, f"GET failed: {get_resp.text}"
    print(f"  -> SUCCESS: Fetched {len(get_resp.json())} records from workspace.")

    # 3. DELETE
    if created_ids:
        target_id = created_ids[0]
        print(f"\n--- 3. Testing DELETE for Record ID {target_id} ---")
        del_resp = requests.delete(f"{BASE_URL}/records/{target_id}")
        assert del_resp.status_code in (200, 204), f"DELETE failed: {del_resp.text}"
        print(f"  -> SUCCESS: Deleted Record ID {target_id}")

    # Negative Test
    print("\n--- Testing Corrupted Endpoint (Negative Test) ---")
    try:
        bad_resp = requests.get(f"{BASE_URL}/records_invalid_route/")
        bad_resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"  -> EXPECTED ERROR CAUGHT! Status {bad_resp.status_code}: {err}")

    print("=== RECORDS INTEGRATION TEST COMPLETED ===\n")

if __name__ == "__main__":
    test_records_api()