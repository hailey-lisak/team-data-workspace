# tests/unit/test_repository.py
# tests/unit/test_repository.py
from unittest.mock import MagicMock
from app.repository import RecordRepository
from app.schemas import RecordIngestRow


def test_bulk_create_records_empty_list():
    mock_db = MagicMock()
    repo = RecordRepository(db_session=mock_db)

    # Pass workspace_id as the second positional argument
    inserted_count = repo.bulk_create_records([], "ws_test_123")

    assert inserted_count == 0
    mock_db.add_all.assert_not_called()


def test_bulk_create_records_success():
    mock_db = MagicMock()
    repo = RecordRepository(db_session=mock_db)

    records = [
        RecordIngestRow(name="Alice", email="alice@example.com", company="Acme"),
        RecordIngestRow(name="Bob", email="bob@example.com", company=None),
    ]

    # Pass workspace_id as the second positional argument
    inserted_count = repo.bulk_create_records(records, "ws_test_123")

    assert inserted_count == 2
    mock_db.add_all.assert_called_once()
    mock_db.commit.assert_called_once()