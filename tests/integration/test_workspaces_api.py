import requests

BASE_URL = "http://localhost:8000"

def test_workspaces_crud():
    print("\n=== STARTING INTEGRATION TEST: WORKSPACES (FULL CRUD) ===")

    # 1. POST (Create)
    ws_payload = {"name": "QA Workspace", "description": "Automated workspace container"}
    print(f"1. Calling POST /workspaces/ for: {ws_payload['name']}")
    create_resp = requests.post(f"{BASE_URL}/workspaces/", json=ws_payload)
    assert create_resp.status_code in (200, 201), f"Create failed: {create_resp.text}"
    workspace_id = create_resp.json()["id"]
    print(f"  -> SUCCESS: Created Workspace ID {workspace_id}")

    # 2. GET (Read)
    print(f"2. Calling GET /workspaces/{workspace_id}")
    get_resp = requests.get(f"{BASE_URL}/workspaces/{workspace_id}")
    assert get_resp.status_code == 200, f"Read failed: {get_resp.text}"
    print(f"  -> SUCCESS: Fetched Workspace {get_resp.json().get('name')}")

    # 3. PATCH/PUT (Update)
    update_payload = {"description": "Updated QA Workspace Description"}
    print(f"3. Calling PATCH /workspaces/{workspace_id}")
    patch_resp = requests.patch(f"{BASE_URL}/workspaces/{workspace_id}", json=update_payload)
    assert patch_resp.status_code == 200, f"Update failed: {patch_resp.text}"
    print(f"  -> SUCCESS: Updated Description to '{patch_resp.json().get('description')}'")

    # 4. DELETE
    print(f"4. Calling DELETE /workspaces/{workspace_id}")
    del_resp = requests.delete(f"{BASE_URL}/workspaces/{workspace_id}")
    assert del_resp.status_code in (200, 204), f"Delete failed: {del_resp.text}"
    print("  -> SUCCESS: Deleted Workspace")

    # Negative Test
    print("\n--- Testing Corrupted Endpoint (Negative Test) ---")
    try:
        bad_resp = requests.get(f"{BASE_URL}/workspaces_corrupted_route/")
        bad_resp.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(f"  -> EXPECTED ERROR CAUGHT! Status {bad_resp.status_code}: {err}")

    print("=== WORKSPACES CRUD INTEGRATION TEST COMPLETED ===\n")

if __name__ == "__main__":
    test_workspaces_crud()