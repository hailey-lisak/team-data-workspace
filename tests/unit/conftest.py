import pytest
from sqlmodel import Session
from database.connection import engine
from database.models import User, Workspace, Record, Job
from database.models import create_user_db, create_workspace_db

TEST_USER_ID = "usr_test_123"
TEST_WORKSPACE_ID = "ws_test_123"
TEST_RECORD_ID = "rec_test_123"
TEST_JOB_ID = "job_test_123"


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session

@pytest.fixture(autouse=True)
def cleanup_test_data(session):
    """Clean up test records in reverse order of foreign key dependencies."""
    # Pre-test cleanup
    for model, item_id in [(Job, TEST_JOB_ID), (Record, TEST_RECORD_ID), (Workspace, TEST_WORKSPACE_ID), (User, TEST_USER_ID)]:
        item = session.get(model, item_id)
        if item:
            session.delete(item)
    session.commit()
    
    yield
    
    # Post-test cleanup
    for model, item_id in [(Job, TEST_JOB_ID), (Record, TEST_RECORD_ID), (Workspace, TEST_WORKSPACE_ID), (User, TEST_USER_ID)]:
        item = session.get(model, item_id)
        if item:
            session.delete(item)
    session.commit()

@pytest.fixture
def sample_workspace_data():
    return {
        "workspace_id": TEST_WORKSPACE_ID,
        "name": "Test Workspace",
        "user_id": TEST_USER_ID,
        "created_at": "2026-01-01T00:00:00"
    }

@pytest.fixture
def sample_record_data():
    return {
        "record_id": TEST_RECORD_ID,
        "workspace_id": TEST_WORKSPACE_ID,
        "name": "Jane Doe",
        "email": "jane@example.com",
        "company": "Acme Corp",
        "city": "Pittsburgh",
        "notes": "Sample note",
        "created_at": "2026-01-01T00:00:00"
    }

@pytest.fixture
def sample_job_data():
    return {
        "job_id": TEST_JOB_ID,
        "workspace_id": TEST_WORKSPACE_ID,
        "status": "pending",
        "total_records": 10,
        "created_at": "2026-01-01T00:00:00"
    }

@pytest.fixture
def sample_user_data():
    return {
        "user_id": "usr_test_123",
        "name": "Test User",
        "email": "test@example.com",
        "created_at": "2026-01-01T00:00:00"  # <-- ADD THIS KEY
    }
@pytest.fixture
def sample_user(db_session):
    user_data = {
        "user_id": "usr_test_123",
        "name": "Test User",
        "email": "test@example.com",
        "created_at": "2026-01-01T00:00:00"
    }
    return create_user_db(db_session, user_data)

@pytest.fixture
def sample_workspace(db_session, sample_user):
    workspace_data = {
        "name": "Test Workspace",
        "owner_id": sample_user.user_id
    }
    return create_workspace_db(db_session, workspace_data)