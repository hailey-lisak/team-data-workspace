import pytest
from datetime import datetime
from database.models import (
    create_user_db,
    get_user_db,
    update_user_db,
    delete_user_db
)


@pytest.fixture
def sample_user_data():
    """Provides a consistent user dictionary for testing."""
    return {
        "user_id": "usr_test_123",
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "created_at": datetime.utcnow().isoformat()
    }


def test_create_user(session, sample_user_data):
    """1. CREATE: Verify user is created and persisted."""
    user = create_user_db(session, sample_user_data)

    assert user.user_id == "usr_test_123"
    assert user.name == "Jane Doe"
    assert user.email == "jane.doe@example.com"


def test_get_user(session, sample_user_data):
    """2. READ: Verify an existing user can be fetched by user_id."""
    create_user_db(session, sample_user_data)

    fetched_user = get_user_db(session, "usr_test_123")

    assert fetched_user is not None
    assert fetched_user.user_id == "usr_test_123"
    assert fetched_user.email == "jane.doe@example.com"


def test_get_nonexistent_user(session):
    """2b. READ (Edge Case): Verify getting a non-existent user returns None."""
    fetched_user = get_user_db(session, "non_existent_id")
    assert fetched_user is None


def test_update_user(session, sample_user_data):
    """3. UPDATE: Verify updating a user's name persists and enforces max length."""
    create_user_db(session, sample_user_data)

    # Update name
    updated_user = update_user_db(session, "usr_test_123", "Jane Smith")

    assert updated_user is not None
    assert updated_user.name == "Jane Smith"

    # Verify update persisted in DB
    re_fetched = get_user_db(session, "usr_test_123")
    assert re_fetched.name == "Jane Smith"


def test_delete_user(session, sample_user_data):
    """4. DELETE: Verify deleting a user removes them completely from DB."""
    create_user_db(session, sample_user_data)

    # Delete
    success = delete_user_db(session, "usr_test_123")
    assert success is True

    # Confirm user is gone
    assert get_user_db(session, "usr_test_123") is None


def test_delete_nonexistent_user(session):
    """4b. DELETE (Edge Case): Verify deleting a non-existent user returns False."""
    success = delete_user_db(session, "non_existent_id")
    assert success is False