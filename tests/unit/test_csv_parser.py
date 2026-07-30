# tests/unit/test_csv_parser.py
from app.csv_parser import parse_and_validate_csv_stream


def test_parse_and_validate_csv_stream_success_and_errors():
    csv_data = (
        "name,email,company,city,notes\n"
        "Alice Smith,alice@example.com,Acme,New York,VIP\n"
        "   ,bob@example.com,Globex,Boston,Standard\n"  # Fails: blank name
    )

    valid, errors = parse_and_validate_csv_stream(csv_data)

    # Row 1 is valid
    assert len(valid) == 1
    assert valid[0].name == "Alice Smith"
    assert valid[0].email == "alice@example.com"

    # Row 2 failed validation
    assert len(errors) == 1
    assert errors[0]["row"] == 2