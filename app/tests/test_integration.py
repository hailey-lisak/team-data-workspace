from fastapi.testclient import TestClient
from app.main import app

# Spin up our virtual web server client
client = TestClient(app)

# ----------------------------------------------------
# 1. CORE / STATUS ENDPOINTS
# ----------------------------------------------------

def test_root_endpoint():
    """GET / -> Test that the home page displays the functional message"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Team Data Workspace API is functional."}


# ----------------------------------------------------
# 2. USER ENDPOINTS
# ----------------------------------------------------

def test_create_user_success():
    """POST /users -> Test successful user creation and Pydantic outputs"""
    payload = {"name": "Alice Smith", "email": "ALICE@example.com"}
    response = client.post("/users", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["name"] == "Alice Smith"
    assert data["email"] == "alice@example.com"  # Verifies service lowered it

def test_create_user_validation_error():
    """POST /users -> Test that a malformed email is blocked by Pydantic"""
    payload = {"name": "Bob", "email": "not-an-email"}
    response = client.post("/users", json=payload)
    assert response.status_code == 422


# ----------------------------------------------------
# 3. WORKSPACE ENDPOINTS
# ----------------------------------------------------

def test_create_workspace_success():
    """POST /workspaces -> Test creating a workspace linked to a user"""
    payload = {"user_id": "usr_12345678"}
    response = client.post("/workspaces", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert "workspace_id" in data
    assert data["workspace_id"].startswith("wsp_")
    assert data["user_id"] == "usr_12345678"


# ----------------------------------------------------
# 4. NESTED WORKSPACE ENDPOINTS (RECORDS & JOBS)
# ----------------------------------------------------

def test_create_record_nested_success():
    """POST /workspaces/{id}/records -> Test processing a pristine record"""
    workspace_id = "wsp_99999999"
    payload = {
        "name": "John Doe",
        "email": "john@b2b.com",
        "company": "Wayne Enterprises",
        "city": "Gotham"
    }
    
    # URL matches your main.py: prefix="/workspaces/{workspace_id}"
    response = client.post(f"/workspaces/{workspace_id}/records", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "completed"
    assert "B2B" in data["tags"]

def test_create_job_nested_success():
    """POST /workspaces/{id}/jobs/process -> Test launching a data job"""
    workspace_id = "wsp_99999999"
    
    # Hit the exact combined URL path your main.py + router sets up
    response = client.post(f"/workspaces/{workspace_id}/jobs/process")
    
    assert response.status_code == 201
    data = response.json()
    assert data["job_id"].startswith("job_")
    assert data["workspace_id"] == "wsp_99999999"
    assert data["status"] == "pending"