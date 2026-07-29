import pytest
from database.models import (
    create_user_db, 
    create_workspace_db, 
    get_workspace_db, 
    update_workspace_db, 
    delete_workspace_db
)

def test_create_workspace(session, sample_user_data, sample_workspace_data):
    create_user_db(session, sample_user_data)  # Parent record required
    ws = create_workspace_db(session, sample_workspace_data)
    assert ws is not None
    assert ws.workspace_id == sample_workspace_data["workspace_id"]
    assert ws.name == sample_workspace_data["name"]

def test_get_workspace(session, sample_user_data, sample_workspace_data):
    create_user_db(session, sample_user_data)
    create_workspace_db(session, sample_workspace_data)
    ws = get_workspace_db(session, sample_workspace_data["workspace_id"])
    assert ws is not None
    assert ws.workspace_id == sample_workspace_data["workspace_id"]

def test_get_nonexistent_workspace(session):
    ws = get_workspace_db(session, "ws_nonexistent_999")
    assert ws is None

def test_update_workspace(session, sample_user_data, sample_workspace_data):
    create_user_db(session, sample_user_data)
    create_workspace_db(session, sample_workspace_data)
    updated = update_workspace_db(session, sample_workspace_data["workspace_id"], "New Workspace Name")
    assert updated is not None
    assert updated.name == "New Workspace Name"

def test_delete_workspace(session, sample_user_data, sample_workspace_data):
    create_user_db(session, sample_user_data)
    create_workspace_db(session, sample_workspace_data)
    deleted = delete_workspace_db(session, sample_workspace_data["workspace_id"])
    assert deleted is True
    assert get_workspace_db(session, sample_workspace_data["workspace_id"]) is None