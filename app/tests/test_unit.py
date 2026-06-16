from app.services.user_services import create_user
from app.services.workspace_services import create_workspace
from app.services.record_services import create_record

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
    result = create_workspace(user_id = "usr_12345678")
    assert result["user_id"] == "usr_12345678"
    assert result["workspace_id"].startswith("wsp_")
def test_record_service_completed_logic():
    '''
    Test that a pristine record gets marked as completed
    '''
    result = create_record(
        name = "Alice Smith",
        email = "alice@gmail.com",
        company = "VRB",
        city = "Pittsburgh"
    )
    assert result["status"] == "completed"
    assert result["error_message"] is None
    assert "B2B" in result["tags"]
    assert "Pittsburgh" in result["tags"]

def test_record_service_rejected_logic():
    '''
    Test that an invalid emial marks the record as rejected
    '''
    result = create_record(
        name="Bob", 
        email="broken-email",
        company = None,
        city = None
    )
    assert result["status"] == "rejected"
    assert "invalid email" in result["error_message"].lower()