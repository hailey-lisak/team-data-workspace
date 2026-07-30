import pytest
from database.models import (
    create_user_db,
    create_workspace_db,
    create_record_db,
    get_record_db,
    delete_record_db,
)


def test_create_record(session, sample_user_data, sample_workspace_data, sample_record_data):
    """Test creating a record associated with a valid workspace and user."""
    # Setup Foreign Key Hierarchy
    create_user_db(session, sample_user_data)
    create_workspace_db(session, sample_workspace_data)

    # Execute Record Creation
    record = create_record_db(session, sample_record_data)

    # Assertions
    assert record is not None
    assert record.record_id == sample_record_data["record_id"]
    assert record.workspace_id == sample_workspace_data["workspace_id"]
    assert record.name == sample_record_data.get("name", "Jane Doe")
    assert record.email == sample_record_data.get("email", "jane@example.com")


def test_get_record(session, sample_user_data, sample_workspace_data, sample_record_data):
    """Test retrieving an existing record by record_id."""
    create_user_db(session, sample_user_data)
    create_workspace_db(session, sample_workspace_data)
    create_record_db(session, sample_record_data)

    record = get_record_db(session, sample_record_data["record_id"])
    assert record is not None
    assert record.record_id == sample_record_data["record_id"]


def test_get_nonexistent_record(session):
    """Test retrieving a record that does not exist returns None."""
    record = get_record_db(session, "non_existent_rec_999")
    assert record is None


def test_delete_record(session, sample_user_data, sample_workspace_data, sample_record_data):
    """Test deleting an existing record."""
    create_user_db(session, sample_user_data)
    create_workspace_db(session, sample_workspace_data)
    create_record_db(session, sample_record_data)

    # Ensure record exists before deleting
    record_id = sample_record_data["record_id"]
    assert get_record_db(session, record_id) is not None

    # Delete record
    success = delete_record_db(session, record_id)
    assert success is True

    # Confirm record is gone
    assert get_record_db(session, record_id) is None


def test_delete_nonexistent_record(session):
    """Test attempting to delete a non-existent record returns False."""
    success = delete_record_db(session, "non_existent_rec_999")
    assert success is False