import uuid
import requests

BASE_URL = "http://localhost:8000"


def test_records_crud():
    print("\n=== STARTING INTEGRATION TEST: RECORDS (FULL CRUD) ===")

    # 0. SETUP: PREREQUISITE USER & WORKSPACE
    random_id = uuid.uuid4().hex[:6]
    
    # Create User
    user_resp = requests.post(
        f"{BASE_URL}/users/",
        json={"email": f"rec_owner_{random_id}@example.com", "name": "Record Owner"},
    )
    assert user_resp.status_code in (200, 201), f"User setup failed: {user_resp.text}"
    user_id = user_resp.json().get("user_id") or user_resp.json().get("id")

    # Create Workspace
    ws_resp = requests.post(
        f"{BASE_URL}/workspaces",
        json={"name": f"WS_For_Records_{random_id}", "user_id": user_id},
    )
    assert ws_resp.status_code in (200, 201), f"Workspace setup failed: {ws_resp.text}"
    workspace_id = ws_resp.json().get("workspace_id") or ws_resp.json().get("id")

    print(f"0. Setup complete: User={user_id}, Workspace={workspace_id}")

    try:
        # 1. CREATE RECORD
        rec_payload = {
            "workspace_id": workspace_id,
            "name": f"Jane Doe {random_id}",
            "email": f"jane_{random_id}@example.com",
            "company": "Acme Corp",
            "city": "New York",
            "notes": "Integration test record",
        }

        print(f"1. Calling POST /workspaces/{workspace_id}/records")
        create_resp = requests.post(
            f"{BASE_URL}/workspaces/{workspace_id}/records", json=rec_payload
        )
        print(f"DEBUG Response ({create_resp.status_code}): {create_resp.text}")

        assert create_resp.status_code in (
            200,
            201,
        ), f"Create record failed: {create_resp.text}"
        created_data = create_resp.json()

        record_id = (
            created_data.get("record_id")
            or created_data.get("id")
            or created_data.get("uuid")
        )
        print(f"   SUCCESS -> Created Record ID: {record_id}")

        # 2. READ (GET RECORD BY ID)
        print(f"2. Calling GET /workspaces/{workspace_id}/records/{record_id}")
        get_resp = requests.get(
            f"{BASE_URL}/workspaces/{workspace_id}/records/{record_id}"
        )
        assert get_resp.status_code == 200, f"Get record failed: {get_resp.text}"
        print(f"   SUCCESS -> Found Record Name: {get_resp.json().get('name')}")

        # 3. DELETE RECORD
        print(f"3. Calling DELETE /workspaces/{workspace_id}/records/{record_id}")
        del_resp = requests.delete(
            f"{BASE_URL}/workspaces/{workspace_id}/records/{record_id}"
        )
        assert del_resp.status_code in (
            200,
            204,
        ), f"Delete record failed: {del_resp.text}"
        print(f"   SUCCESS -> Deleted Record ID: {record_id}")

    finally:
        # CLEANUP: DELETE WORKSPACE & USER
        print(f"4. Cleaning up Workspace ({workspace_id}) and User ({user_id})")
        requests.delete(f"{BASE_URL}/workspaces/{workspace_id}")
        requests.delete(f"{BASE_URL}/users/{user_id}")

    print("\nALL RECORD INTEGRATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_records_crud()