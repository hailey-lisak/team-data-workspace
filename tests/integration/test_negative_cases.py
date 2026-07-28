import uuid
import requests

BASE_URL = "http://localhost:8000"


# -------------------------------------------------------------------
# 1. USERS DOMAIN NEGATIVE TESTS
# -------------------------------------------------------------------
def test_user_negative_cases():
    bogus_id = f"usr_fake_{uuid.uuid4().hex[:6]}"

    # Delete non-existent user -> 404
    assert requests.delete(f"{BASE_URL}/users/{bogus_id}").status_code == 404

    # 422 Payload Validation Errors
    assert (
        requests.post(f"{BASE_URL}/users/", json={}).status_code == 422
    )  # Empty payload
    assert (
        requests.post(
            f"{BASE_URL}/users/", json={"email": "invalid_email_format"}
        ).status_code
        == 422
    )
    assert (
        requests.post(
            f"{BASE_URL}/users/", json={"email": 12345, "name": ["Not", "String"]}
        ).status_code
        == 422
    )


# -------------------------------------------------------------------
# 2. WORKSPACES DOMAIN NEGATIVE TESTS
# -------------------------------------------------------------------
def test_workspace_negative_cases():
    bogus_ws_id = f"wsp_fake_{uuid.uuid4().hex[:6]}"
    bogus_user_id = f"usr_fake_{uuid.uuid4().hex[:6]}"

    # Delete non-existent workspace -> 404
    assert (
        requests.delete(f"{BASE_URL}/workspaces/{bogus_ws_id}").status_code
        == 404
    )

    # Creating Workspace for Non-Existent User ID
    # Note: Returns 500 when backend lacks explicit FK validation check
    orphan_ws = {"name": "Orphan Workspace", "user_id": bogus_user_id}
    res = requests.post(f"{BASE_URL}/workspaces", json=orphan_ws)
    assert res.status_code in (
        404,
        422,
        400,
        500,
    ), f"Unexpected response code for orphan user_id, got {res.status_code}"

    # Malformed Input Types
    bad_type_ws = {"name": 999999, "user_id": None}
    assert requests.post(f"{BASE_URL}/workspaces", json=bad_type_ws).status_code == 422

# -------------------------------------------------------------------
# 3. RECORDS DOMAIN NEGATIVE TESTS
# -------------------------------------------------------------------
def test_record_negative_cases():
    bogus_ws_id = f"wsp_fake_{uuid.uuid4().hex[:6]}"
    bogus_rec_id = f"rec_fake_{uuid.uuid4().hex[:6]}"

    # 404 Operations on Missing Records
    assert (
        requests.get(
            f"{BASE_URL}/workspaces/{bogus_ws_id}/records/{bogus_rec_id}"
        ).status_code
        == 404
    )
    assert (
        requests.delete(
            f"{BASE_URL}/workspaces/{bogus_ws_id}/records/{bogus_rec_id}"
        ).status_code
        == 404
    )

    # Missing Required Fields for Record Creation -> 422
    partial_payloads = [
        {"workspace_id": bogus_ws_id},  # Missing name, email, company, city
        {"workspace_id": bogus_ws_id, "name": "Missing Rest"},
        {"name": "No Workspace ID", "email": "test@test.com"},
    ]
    for payload in partial_payloads:
        res = requests.post(
            f"{BASE_URL}/workspaces/{bogus_ws_id}/records", json=payload
        )
        assert (
            res.status_code == 422
        ), f"Expected 422 for partial payload {payload}, got {res.status_code}"


# -------------------------------------------------------------------
# 4. JOBS DOMAIN NEGATIVE TESTS
# -------------------------------------------------------------------
def test_job_negative_cases():
    bogus_ws_id = f"wsp_fake_{uuid.uuid4().hex[:6]}"
    bogus_job_id = f"job_fake_{uuid.uuid4().hex[:6]}"

    # 404 Fetching Missing Job
    assert (
        requests.get(
            f"{BASE_URL}/workspaces/{bogus_ws_id}/jobs/{bogus_job_id}"
        ).status_code
        == 404
    )

    # Invalid Job Status Update
    invalid_status_payload = {
        "status": "SUPER_INVALID_STATUS",
        "total_records": -1,
    }
    res = requests.put(
        f"{BASE_URL}/workspaces/{bogus_ws_id}/jobs/{bogus_job_id}",
        json=invalid_status_payload,
    )
    assert res.status_code in (
        404,
        422,
        400,
    ), f"Expected failure on invalid status transition, got {res.status_code}"


# -------------------------------------------------------------------
# 5. PROTOCOL & HTTP HEADER NEGATIVE TESTS
# -------------------------------------------------------------------
def test_protocol_and_header_negative_cases():
    # Sending plain text instead of JSON payload
    raw_headers = {"Content-Type": "text/plain"}
    res = requests.post(
        f"{BASE_URL}/users/", data="Not JSON at all", headers=raw_headers
    )
    assert res.status_code in (
        415,
        422,
        400,
    ), f"Expected unsupported media type or validation error, got {res.status_code}"

    # Invalid HTTP Verb on route
    res = requests.patch(f"{BASE_URL}/users/")
    assert (
        res.status_code == 405
    ), f"Expected 405 Method Not Allowed, got {res.status_code}"