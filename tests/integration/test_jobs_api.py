import uuid
import requests

BASE_URL = "http://localhost:8000"


def test_jobs_crud():
    print("\n=== STARTING INTEGRATION TEST: JOBS (FULL CRUD) ===")

    # 0. SETUP: PREREQUISITE USER & WORKSPACE
    random_id = uuid.uuid4().hex[:6]

    # Create User
    user_resp = requests.post(
        f"{BASE_URL}/users/",
        json={"email": f"job_owner_{random_id}@example.com", "name": "Job Owner"},
    )
    assert user_resp.status_code in (200, 201), f"User setup failed: {user_resp.text}"
    user_id = user_resp.json().get("user_id") or user_resp.json().get("id")

    # Create Workspace
    ws_resp = requests.post(
        f"{BASE_URL}/workspaces",
        json={"name": f"WS_For_Jobs_{random_id}", "user_id": user_id},
    )
    assert ws_resp.status_code in (200, 201), f"Workspace setup failed: {ws_resp.text}"
    workspace_id = ws_resp.json().get("workspace_id") or ws_resp.json().get("id")

    print(f"0. Setup complete: User={user_id}, Workspace={workspace_id}")

    try:
        # 1. CREATE JOB
        job_payload = {"workspace_id": workspace_id}

        print(f"1. Calling POST /workspaces/{workspace_id}/jobs")
        create_resp = requests.post(
            f"{BASE_URL}/workspaces/{workspace_id}/jobs", json=job_payload
        )
        print(f"DEBUG Response ({create_resp.status_code}): {create_resp.text}")

        assert create_resp.status_code in (
            200,
            201,
        ), f"Create job failed: {create_resp.text}"
        created_data = create_resp.json()

        job_id = (
            created_data.get("job_id")
            or created_data.get("id")
            or created_data.get("uuid")
        )
        print(f"   SUCCESS -> Created Job ID: {job_id}")

        # 2. READ (GET JOB BY ID)
        print(f"2. Calling GET /workspaces/{workspace_id}/jobs/{job_id}")
        get_resp = requests.get(
            f"{BASE_URL}/workspaces/{workspace_id}/jobs/{job_id}"
        )
        assert get_resp.status_code == 200, f"Get job failed: {get_resp.text}"
        print(f"   SUCCESS -> Found Job Status: {get_resp.json().get('status')}")

        # 3. UPDATE JOB STATUS
        update_payload = {
            "status": "completed",
            "total_records": 100,
            "error_message": "",
        }
        print(f"3. Calling PUT /workspaces/{workspace_id}/jobs/{job_id}")
        put_resp = requests.put(
            f"{BASE_URL}/workspaces/{workspace_id}/jobs/{job_id}",
            json=update_payload,
        )
        assert put_resp.status_code == 200, f"Update job failed: {put_resp.text}"
        print(
            f"   SUCCESS -> Updated Job Status: {put_resp.json().get('status')}"
        )

    finally:
        # CLEANUP: DELETE WORKSPACE & USER
        print(f"4. Cleaning up Workspace ({workspace_id}) and User ({user_id})")
        requests.delete(f"{BASE_URL}/workspaces/{workspace_id}")
        requests.delete(f"{BASE_URL}/users/{user_id}")

    print("\nALL JOB INTEGRATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_jobs_crud()