import pytest
from pydantic import ValidationError
from app.api.records import RecordCreateRequest


# ==========================================
# 1. HAPPY PATH & DEFAULTS
# ==========================================

def test_record_create_request_valid_full_payload():
    """Validates that a complete, well-formed payload parses correctly."""
    payload = {
        "workspace_id": "wsp_12345678",
        "name": "Jane Doe",
        "email": "jane@example.com",
        "company": "Tech Corp",
        "city": "Austin",
        "notes": "VIP Client - High Priority"
    }
    req = RecordCreateRequest(**payload)
    
    assert req.workspace_id == "wsp_12345678"
    assert req.name == "Jane Doe"
    assert req.email == "jane@example.com"
    assert req.company == "Tech Corp"
    assert req.city == "Austin"
    assert req.notes == "VIP Client - High Priority"


def test_record_create_request_default_notes():
    """Ensures 'notes' defaults to an empty string when omitted."""
    payload = {
        "workspace_id": "wsp_12345678",
        "name": "Jane Doe",
        "email": "jane@example.com",
        "company": "Tech Corp",
        "city": "Austin"
    }
    req = RecordCreateRequest(**payload)
    assert req.notes == ""


# ==========================================
# 2. REQUIRED FIELDS & MISSING KEYS
# ==========================================

@pytest.mark.parametrize("required_field", [
    "workspace_id", 
    "name", 
    "email", 
    "company", 
    "city"
])
def test_record_create_request_missing_required_fields(required_field):
    """Verifies that omitting any required field triggers a ValidationError."""
    payload = {
        "workspace_id": "wsp_12345678",
        "name": "Jane Doe",
        "email": "jane@example.com",
        "company": "Tech Corp",
        "city": "Austin"
    }
    del payload[required_field]
    
    with pytest.raises(ValidationError) as exc_info:
        RecordCreateRequest(**payload)
    
    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"][0] == required_field


def test_record_create_request_empty_payload():
    """Verifies that passing an empty dictionary fails with all missing field errors."""
    with pytest.raises(ValidationError) as exc_info:
        RecordCreateRequest(**{})
    assert len(exc_info.value.errors()) >= 5


# ==========================================
# 3. DATA TYPES & TYPE COERCION
# ==========================================

@pytest.mark.parametrize("invalid_value", [
    ["Jane", "Doe"],            # List
    {"first": "Jane"},          # Dict
    None,                       # None/Null
])
def test_record_create_request_invalid_field_types(invalid_value):
    """Rejects non-string complex data structures passed to string fields."""
    payload = {
        "workspace_id": "wsp_12345678",
        "name": invalid_value,
        "email": "jane@example.com",
        "company": "Tech Corp",
        "city": "Austin"
    }
    with pytest.raises(ValidationError):
        RecordCreateRequest(**payload)


def test_record_create_request_coerces_numbers_to_strings():
    """Pydantic v2 automatically coerces integers/floats to strings if safe."""
    payload = {
        "workspace_id": 12345678,  # Int instead of str
        "name": "Jane Doe",
        "email": "jane@example.com",
        "company": 100,            # Int instead of str
        "city": "Austin"
    }
    req = RecordCreateRequest(**payload)
    assert req.workspace_id == "12345678"
    assert req.company == "100"


# ==========================================
# 4. EDGE CASES & SPECIAL CHARACTER INPUTS
# ==========================================

def test_record_create_request_handles_unicode_and_emojis():
    """Ensures international names, accents, and emojis pass validation without crashing."""
    payload = {
        "workspace_id": "wsp_999",
        "name": "François-Müller 👋",
        "email": "muller@domain.de",
        "company": "Société Générale",
        "city": "São Paulo",
        "notes": "⚡️ Priority account"
    }
    req = RecordCreateRequest(**payload)
    assert req.name == "François-Müller 👋"
    assert req.city == "São Paulo"


def test_record_create_request_ignores_extra_payload_fields():
    """Guards against extra field injections (ignores unexpected properties)."""
    payload = {
        "workspace_id": "wsp_12345678",
        "name": "Jane Doe",
        "email": "jane@example.com",
        "company": "Tech Corp",
        "city": "Austin",
        "admin_role": "superadmin",
        "is_active": True
    }
    req = RecordCreateRequest(**payload)
    assert not hasattr(req, "admin_role")
    assert not hasattr(req, "is_active")