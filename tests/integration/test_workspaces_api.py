import uuid
import requests

BASE_URL = "http://localhost:8000"


def test_workspaces_crud():
    print("\n=== STARTING INTEGRATION TEST: WORKSPACES (FULL CRUD) ===")

    # 0. SETUP: CREATE A USER TO OWN THE WORKSPACE
    random_user_id = uuid.uuid4().hex[:6]
    test_email = f"ws_owner_{random_user_id}@example.com"
    print(f"0. Creating prerequisite user: {test_email}")
    user_resp = requests.post(
        f"{BASE_URL}/users/", json={"email": test_email, "name": "Workspace Owner"}
    )
    assert user_resp.status_code in (200, 201), f"User setup failed: {user_resp.text}"
    owner_user_id = user_resp.json().get("user_id") or user_resp.json().get("id")
    print(f"   SUCCESS -> Created Owner User ID: {owner_user_id}")

    try:
        # 1. CREATE WORKSPACE
        random_id = uuid.uuid4().hex[:6]
        ws_name = f"Workspace_{random_id}"
        ws_payload = {"name": ws_name, "user_id": owner_user_id}

        print(f"1. Calling POST /workspaces for: {ws_name}")
        create_resp = requests.post(f"{BASE_URL}/workspaces", json=ws_payload)
        print(f"DEBUG Response ({create_resp.status_code}): {create_resp.text}")

        assert create_resp.status_code in (
            200,
            201,
        ), f"Create failed: {create_resp.text}"
        created_data = create_resp.json()

        ws_id = created_data.get("workspace_id") or created_data.get("id")
        print(f"   SUCCESS -> Created Workspace ID: {ws_id}")

        # 2. READ (GET ALL WORKSPACES)
        print(f"2. Calling GET /workspaces")
        get_resp = requests.get(f"{BASE_URL}/workspaces")
        assert get_resp.status_code == 200, f"Get failed: {get_resp.text}"

        workspaces_list = get_resp.json()
        matching_ws = next(
            (
                w
                for w in workspaces_list
                if (w.get("workspace_id") == ws_id or w.get("id") == ws_id)
            ),
            None,
        )
        assert (
            matching_ws is not None
        ), f"Workspace {ws_id} not found in workspaces list!"
        print(f"   SUCCESS -> Found Workspace in list: {matching_ws.get('name')}")

        # 3. UPDATE WORKSPACE
        update_payload = {"name": f"Updated_{ws_name}", "user_id": owner_user_id}
        print(f"3. Calling PUT /workspaces/{ws_id}")
        put_resp = requests.put(
            f"{BASE_URL}/workspaces/{ws_id}", json=update_payload
        )
        assert put_resp.status_code == 200, f"Update failed: {put_resp.text}"
        print(
            f"   SUCCESS -> Updated Workspace Name: {put_resp.json().get('name')}"
        )

        # 4. DELETE WORKSPACE
        print(f"4. Calling DELETE /workspaces/{ws_id}")
        del_resp = requests.delete(f"{BASE_URL}/workspaces/{ws_id}")
        assert del_resp.status_code in (
            200,
            204,
        ), f"Delete failed: {del_resp.text}"
        print(f"   SUCCESS -> Deleted Workspace ID: {ws_id}")

    finally:
        # CLEANUP: DELETE PREREQUISITE USER
        print(f"5. Cleaning up prerequisite user {owner_user_id}")
        requests.delete(f"{BASE_URL}/users/{owner_user_id}")

    print("\nALL WORKSPACE INTEGRATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_workspaces_crud()