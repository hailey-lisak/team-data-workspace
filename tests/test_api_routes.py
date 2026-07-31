import os
import uuid
import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def test_records_api_isolated_operations():
    print("\n" + "=" * 60)
    print("STARTING ISOLATED RECORDS API TESTS")
    print("=" * 60)

    unique_suffix = uuid.uuid4().hex[:6]

    # Setup temporary User & Workspace to hold records
    user_res = requests.post(
        f"{BASE_URL}/users",
        json={"email": f"rec_tester_{unique_suffix}@example.com", "name": "Record Tester"},
    )
    user_id = user_res.json().get("user_id") or user_res.json().get("id")

    ws_res = requests.post(
        f"{BASE_URL}/workspaces",
        json={"name": f"Record_Test_WS_{unique_suffix}", "user_id": user_id},
    )
    workspace_id = ws_res.json().get("workspace_id") or ws_res.json().get("id")

    try:
        # 1. POST Single Record (JSON payload)
        print("\n[1] Testing POST /workspaces/{workspace_id}/records...")
        record_payload = {
            "workspace_id": workspace_id,
            "name": "Single Record Test",
            "email": f"single_{unique_suffix}@example.com",
            "company": "Test Co",
            "city": "Austin",
            "notes": "Testing single JSON create",
        }
        create_res = requests.post(
            f"{BASE_URL}/workspaces/{workspace_id}/records",
            json=record_payload,
        )
        assert create_res.status_code in (200, 201), f"Create record failed: {create_res.text}"
        
        record_data = create_res.json()
        record_id = record_data.get("id") or record_data.get("record_id")
        print(f"  ✓ Created record ID: {record_id}")

        # 2. GET Record by ID
        print(f"\n[2] Testing GET /workspaces/{{workspace_id}}/records/{record_id}...")
        get_res = requests.get(f"{BASE_URL}/workspaces/{workspace_id}/records/{record_id}")
        assert get_res.status_code == 200, f"GET record failed: {get_res.text}"
        print(f"  ✓ Successfully retrieved record: {get_res.json().get('email')}")

        # 3. GET Non-Existent Record (404 Negative Test)
        print("\n[3] Testing GET with invalid Record ID (Expecting 404)...")
        bad_get = requests.get(f"{BASE_URL}/workspaces/{workspace_id}/records/non_existent_id_9999")
        assert bad_get.status_code == 404, f"Expected 404, got: {bad_get.status_code}"
        print("  ✓ Correctly received 404 Not Found")

        # 4. DELETE Record
        print(f"\n[4] Testing DELETE /workspaces/{{workspace_id}}/records/{record_id}...")
        del_res = requests.delete(f"{BASE_URL}/workspaces/{workspace_id}/records/{record_id}")
        assert del_res.status_code in (200, 204), f"Delete record failed: {del_res.text}"
        print("  ✓ Successfully deleted record")

        # 5. Verify Record is Gone
        verify_get = requests.get(f"{BASE_URL}/workspaces/{workspace_id}/records/{record_id}")
        assert verify_get.status_code == 404, "Record still exists after deletion!"
        print("  ✓ Confirmed record no longer exists in DB")

        print("\n" + "=" * 60)
        print("ALL ISOLATED RECORD TESTS PASSED GREEN!")
        print("=" * 60)

    finally:
        # Teardown parent container
        if workspace_id:
            requests.delete(f"{BASE_URL}/workspaces/{workspace_id}")
        if user_id:
            requests.delete(f"{BASE_URL}/users/{user_id}")


if __name__ == "__main__":
    test_records_api_isolated_operations()