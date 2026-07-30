import pytest
from database.models import (
    create_user_db,
    create_workspace_db,
    create_job_db,
    get_job_db,
    update_job_status_db,
)


def test_create_job(session, sample_user_data, sample_workspace_data, sample_job_data):
    """Test creating a job under a valid workspace and user."""
    create_user_db(session, sample_user_data)
    create_workspace_db(session, sample_workspace_data)

    job = create_job_db(session, sample_job_data)

    assert job is not None
    assert job.job_id == sample_job_data["job_id"]
    assert job.workspace_id == sample_workspace_data["workspace_id"]
    assert job.status == "pending"


def test_get_job(session, sample_user_data, sample_workspace_data, sample_job_data):
    """Test fetching an existing job by job_id."""
    create_user_db(session, sample_user_data)
    create_workspace_db(session, sample_workspace_data)
    create_job_db(session, sample_job_data)

    job = get_job_db(session, sample_job_data["job_id"])
    assert job is not None
    assert job.job_id == sample_job_data["job_id"]


def test_get_nonexistent_job(session):
    """Test retrieving a non-existent job returns None."""
    job = get_job_db(session, "non_existent_job_999")
    assert job is None


def test_update_job_status(session, sample_user_data, sample_workspace_data, sample_job_data):
    """Test updating a job's status (e.g. pending -> completed)."""
    create_user_db(session, sample_user_data)
    create_workspace_db(session, sample_workspace_data)
    create_job_db(session, sample_job_data)

    updated_job = update_job_status_db(session, sample_job_data["job_id"], "completed")

    assert updated_job is not None
    assert updated_job.status == "completed"


def test_update_nonexistent_job_status(session):
    """Test updating status on a non-existent job returns None."""
    updated_job = update_job_status_db(session, "non_existent_job_999", "completed")
    assert updated_job is None