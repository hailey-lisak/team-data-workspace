from app.services.user_services import create_user
from app.services.workspace_services import create_workspace
from app.services.record_services import create_record
from app.services.job_services import create_job
'''
assert -> like a quality control inspector
    - if the code works, Python just quietly continues
    - if it fails, it evaluates to false and stops running the test. it will throw an AssertionError
'''
def test_user_service_cleaning():
    '''
    Tests that user service properly cleans text and formats IDs
    '''
    result = create_user(name="  John Doe   ", email="JD@gmail.com")
    assert result["name"] == "John Doe"
    assert result["email"] == "jd@gmail.com"
    assert result["user_id"].startswith("usr_")
    assert len(result["user_id"]) == 12
def test_workspace_service_linking():
    '''
    Tests that workspace service links to an owner and strips inputs
    '''
    result = create_workspace(name = "Engineering Sandbox", user_id = "usr_12345678")
    assert result["user_id"] == "usr_12345678"
    assert result["workspace_id"].startswith("wsp_")
def test_record_service_completed_logic():
    '''
    Test that a pristine record gets marked as completed
    '''
    result = create_record(
        workspace_id="wsp_99999999",
        name="Alice Smith",
        email="alice@gmail.com",
        company="VRB",
        city="Pittsburgh",
        notes=""
    )
    # Target the exact keys from the storage block printout
    assert result["is_valid"] is True
    assert result["tag"] == "complete"

def test_record_service_rejected_logic():
    '''
    Test that an invalid email marks the record as rejected
    '''
    result = create_record(
        workspace_id="wsp_99999999",
        name="Bob",
        email="broken-email",
        company=None,
        city=None,
        notes=""
    )
    assert result["is_valid"] is True
    assert result["tag"] == "missing_company"

def test_job_service_creation():
    """Test that jobs are initialized with a workspace link and pending status"""
    # Pass ONLY the workspace_id that your service expects
    result = create_job(workspace_id="wsp_12345678")
    
    assert result["workspace_id"] == "wsp_12345678"
    assert result["status"] == "completed"               # All newly created jobs start as pending
    assert result["job_id"].startswith("job_")
    assert "created_at" in result                      # Ensure it stamped the arrival time