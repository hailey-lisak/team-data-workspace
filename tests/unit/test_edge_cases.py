import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from database.models import (
    # User services
    create_user_db,
    get_user_db,
    update_user_db,
    delete_user_db,
    # Workspace services
    create_workspace_db,
    get_workspace_db,
    update_workspace_db,
    delete_workspace_db,
    # Record services (Immutable: Create, Get, Delete only)
    create_record_db,
    get_record_db,
    delete_record_db,
    # Job services (Permanent: Create, Get, Update Status only)
    create_job_db,
    get_job_db,
    update_job_status_db,
)


# ============================================================================
# USER SERVICE EDGE CASES
# ============================================================================

def test_create_user_duplicate_email(session, sample_user_data):
    """Test creating two users with the same email triggers a unique constraint error."""
    create_user_db(session, sample_user_data)

    duplicate_user_data = sample_user_data.copy()
    duplicate_user_data["user_id"] = "usr_different_id_999"

    with pytest.raises(IntegrityError):
        create_user_db(session, duplicate_user_data)

    session.rollback()


def test_create_user_invalid_datetime(session, sample_user_data):
    """Test creating a user with an invalid datetime string triggers a ValueError or ValidationError."""
    sample_user_data["created_at"] = "not-a-valid-date"

    with pytest.raises((ValueError, ValidationError)):
        create_user_db(session, sample_user_data)


def test_get_nonexistent_user(session):
    """Test fetching a non-existent user returns None cleanly."""
    user = get_user_db(session, "usr_ghost_999")
    assert user is None


def test_update_nonexistent_user(session):
    """Test updating a user that does not exist returns None."""
    updated_user = update_user_db(session, "usr_ghost_999", {"name": "Ghost"})
    assert updated_user is None


def test_delete_nonexistent_user(session):
    """Test deleting a non-existent user returns False or None safely."""
    result = delete_user_db(session, "usr_ghost_999")
    assert result is False or result is None


# ============================================================================
# WORKSPACE SERVICE EDGE CASES
# ============================================================================

def test_create_workspace_invalid_user_fk(session, sample_workspace_data):
    """Test creating a workspace referencing a non-existent user_id fails foreign key constraint."""
    sample_workspace_data["user_id"] = "usr_ghost_999"

    with pytest.raises(IntegrityError):
        create_workspace_db(session, sample_workspace_data)

    session.rollback()


def test_create_workspace_invalid_datetime(session, sample_workspace_data):
    """Test creating a workspace with an invalid ISO datetime string raises ValueError or ValidationError."""
    sample_workspace_data["created_at"] = "bad-iso-timestamp"

    with pytest.raises((ValueError, ValidationError)):
        create_workspace_db(session, sample_workspace_data)


def test_get_nonexistent_workspace(session):
    """Test fetching a non-existent workspace returns None."""
    workspace = get_workspace_db(session, "ws_ghost_999")
    assert workspace is None


def test_update_nonexistent_workspace(session):
    """Test updating a workspace that does not exist returns None."""
    result = update_workspace_db(session, "ws_ghost_999", {"name": "New Name"})
    assert result is None


def test_delete_nonexistent_workspace(session):
    """Test deleting a non-existent workspace returns False cleanly."""
    result = delete_workspace_db(session, "ws_ghost_999")
    assert result is False or result is None


# ============================================================================
# RECORD SERVICE EDGE CASES (Records are immutable — No Updates)
# ============================================================================

def test_create_record_invalid_workspace_fk(session, sample_record_data):
    """Test creating a record referencing a non-existent workspace_id raises IntegrityError."""
    sample_record_data["workspace_id"] = "ws_ghost_999"

    with pytest.raises(IntegrityError):
        create_record_db(session, sample_record_data)

    session.rollback()


def test_create_record_invalid_datetime(session, sample_record_data):
    """Test creating a record with an unparseable timestamp raises ValueError or ValidationError."""
    sample_record_data["created_at"] = "2026-13-45"

    with pytest.raises((ValueError, ValidationError)):
        create_record_db(session, sample_record_data)


def test_get_nonexistent_record(session):
    """Test getting a non-existent record returns None."""
    record = get_record_db(session, "rec_ghost_999")
    assert record is None


def test_delete_nonexistent_record(session):
    """Test deleting a non-existent record returns False cleanly."""
    result = delete_record_db(session, "rec_ghost_999")
    assert result is False or result is None


# ============================================================================
# JOB SERVICE EDGE CASES (Jobs cannot be deleted)
# ============================================================================

def test_create_job_invalid_workspace_fk(session, sample_job_data):
    """Test creating a job with a non-existent workspace_id triggers an IntegrityError."""
    sample_job_data["workspace_id"] = "ws_ghost_999"

    with pytest.raises(IntegrityError):
        create_job_db(session, sample_job_data)

    session.rollback()


def test_create_job_invalid_datetime(session, sample_job_data):
    """Test creating a job with an invalid ISO datetime string raises ValueError or ValidationError."""
    sample_job_data["created_at"] = "invalid-date-string"

    with pytest.raises((ValueError, ValidationError)):
        create_job_db(session, sample_job_data)


def test_get_nonexistent_job(session):
    """Test fetching a non-existent job returns None."""
    job = get_job_db(session, "job_ghost_999")
    assert job is None


def test_update_job_status_with_error_message(
    session, sample_user_data, sample_workspace_data, sample_job_data
):
    """Test updating a job status to 'failed' while recording an error message string."""
    create_user_db(session, sample_user_data)
    create_workspace_db(session, sample_workspace_data)
    create_job_db(session, sample_job_data)

    error_txt = "Pipeline run failed due to network timeout."

    # Using positional parameters to avoid keyword argument mismatches
    job = update_job_status_db(
        session,
        sample_job_data["job_id"],
        "failed",
        error_message=error_txt,
    )

    assert job is not None
    assert job.status == "failed"
    assert job.error_message == error_txt


def test_update_status_nonexistent_job(session):
    """Test updating status on a non-existent job cleanly returns None."""
    # Using positional parameters to avoid keyword argument mismatches
    result = update_job_status_db(session, "job_ghost_999", "completed")
    assert result is None