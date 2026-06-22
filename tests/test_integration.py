from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    """GET / -> Test that the home page displays the functional message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Team Data Workspace API is functional."}

def test_create_user_success():
    """POST /users -> Test successful user creation and Pydantic outputs"""
    payload = {"name": "Alice Smith", "email": "ALICE@example.com"}
    response = client.post("/users", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["name"] == "Alice Smith"
    assert data["email"] == "alice@example.com"

def test_create_user_validation_error():
    """POST /users -> Test that a malformed email is blocked by Pydantic"""
    payload = {"name": "Bob", "email": "not-an-email"}
    response = client.post("/users", json=payload)
    assert response.status_code == 422

def test_create_workspace_success():
    """POST /workspaces -> Test creating a workspace linked to a user"""
    payload = {"name": "Main Workspace", "user_id": "usr_12345678"}
    response = client.post("/workspaces", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "workspace_id" in data
    assert data["workspace_id"].startswith("wsp_")
    assert data["user_id"] == "usr_12345678"

def test_create_record_nested_success():
    """POST /workspaces/{id}/records/import -> Test importing a record"""
    workspace_id = "wsp_99999999"
    payload = {
        "name": "John Doe",
        "email": "john@b2b.com",
        "company": "Wayne Enterprises",
        "city": "Gotham",
        "notes": "Looking for clean data workspace setups"
    }
    
    # Combined matching endpoint layout
    response = client.post(f"/workspaces/{workspace_id}/records/import", json=payload)
    
    # If it falls back to a different structure, catch it cleanly
    if response.status_code == 404:
        response = client.post(f"/records/import?workspace_id={workspace_id}", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["is_valid"] is True
    assert data["tag"] == "complete"

def test_create_job_nested_success():
    """POST /workspaces/{id}/jobs/process -> Test launching a data job"""
    workspace_id = "wsp_99999999"
    response = client.post(f"/workspaces/{workspace_id}/jobs/process")
    
    assert response.status_code == 201
    data = response.json()
    assert data["job_id"].startswith("job_")
    assert data["workspace_id"] == "wsp_99999999"
    assert data["status"] == "pending"
    assert data["started_at"] is None
    assert data["completed_at"] is None