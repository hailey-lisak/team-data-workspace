import uuid
import requests

BASE_URL = "http://localhost:8000"


def test_users_crud():
    print("\n=== STARTING INTEGRATION TEST: USERS (FULL CRUD) ===")

    # 1. CREATE USER
    random_id = uuid.uuid4().hex[:6]
    test_email = f"user_{random_id}@example.com"
    user_payload = {"email": test_email, "name": "Test User"}

    print(f"1. Calling POST /users/ for: {test_email}")
    create_resp = requests.post(f"{BASE_URL}/users/", json=user_payload)
    print(f"DEBUG Response ({create_resp.status_code}): {create_resp.text}")

    assert create_resp.status_code in (
        200,
        201,
    ), f"Create failed: {create_resp.text}"
    created_data = create_resp.json()

    user_id = created_data.get("user_id") or created_data.get("id")
    print(f"   SUCCESS -> Created User ID: {user_id}")

    # 2. READ (GET ALL USERS)
    print(f"2. Calling GET /users")
    get_resp = requests.get(f"{BASE_URL}/users")
    assert get_resp.status_code == 200, f"Get failed: {get_resp.text}"

    users_list = get_resp.json()
    matching_user = next(
        (u for u in users_list if u.get("user_id") == user_id), None
    )
    assert matching_user is not None, f"User {user_id} not found in user list!"
    print(f"   SUCCESS -> Found User in list: {matching_user.get('email')}")

    # 3. UPDATE (PUT USER)
    update_payload = {"email": test_email, "name": "Updated Test User"}
    print(f"3. Calling PUT /users/{user_id}")
    put_resp = requests.put(
        f"{BASE_URL}/users/{user_id}", json=update_payload
    )
    assert put_resp.status_code == 200, f"Update failed: {put_resp.text}"
    print(f"   SUCCESS -> Updated Name: {put_resp.json().get('name')}")

    # 4. DELETE USER
    print(f"4. Calling DELETE /users/{user_id}")
    del_resp = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert del_resp.status_code in (
        200,
        204,
    ), f"Delete failed: {del_resp.text}"
    print(f"   SUCCESS -> Deleted User ID: {user_id}")

    print("\nALL USER INTEGRATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_users_crud()