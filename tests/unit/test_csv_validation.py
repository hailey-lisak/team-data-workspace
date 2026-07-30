# tests/unit/test_schemas.py
import pytest
from pydantic import ValidationError
from app.schemas import RecordIngestRow


def test_valid_record_ingest_row():
    data = {
        "name": "Alice Smith",
        "email": "alice@example.com",
        "company": "Acme Corp",
        "city": "New York",
        "notes": "VIP Client",
    }
    row = RecordIngestRow(**data)

    assert row.name == "Alice Smith"
    assert row.email == "alice@example.com"
    assert row.company == "Acme Corp"


def test_whitespace_stripping_and_empty_to_none():
    data = {
        "name": "  Bob  ",
        "email": " bob@example.com ",
        "company": "   ",  # Whitespace-only string -> converted to None
        "city": "",  # Empty string -> converted to None
        "notes": "  Some note  ",
    }
    row = RecordIngestRow(**data)

    assert row.name == "Bob"
    assert row.email == "bob@example.com"
    assert row.company is None
    assert row.city is None
    assert row.notes == "Some note"


def test_missing_required_fields_raises_validation_error():
    data = {
        "name": "   ",  # Fails min_length=1 after strip
        "email": "alice@example.com",
    }

    with pytest.raises(ValidationError):
        RecordIngestRow(**data)

