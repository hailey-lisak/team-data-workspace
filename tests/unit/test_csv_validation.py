import io
import csv
import pytest


def parse_raw_csv_text(contents: str) -> list[dict]:
    """
    Replicates the exact CSV parsing loop from your endpoint:
    contents = file.file.read().decode("utf-8")
    buffer = io.StringIO(contents)
    reader = csv.DictReader(buffer)
    """
    buffer = io.StringIO(contents)
    reader = csv.DictReader(buffer)
    parsed_rows = []

    for row in reader:
        # Your exact empty-row check from records.py
        if not any(val and val.strip() for val in row.values()):
            continue
            
        parsed_rows.append({
            "name": row.get("name", ""),
            "email": row.get("email", ""),
            "company": row.get("company", ""),
            "city": row.get("city", ""),
            "notes": row.get("notes", "")
        })
        
    return parsed_rows


# ==========================================
# 1. STANDARD PARSING & CLEAN DATA
# ==========================================

def test_csv_parser_valid_multiple_rows():
    """Verifies clean multi-row CSV parsing."""
    csv_text = (
        "name,email,company,city,notes\n"
        "Alice,alice@example.com,Acme Corp,NYC,Lead\n"
        "Bob,bob@example.com,Beta Inc,LA,Customer\n"
    )
    rows = parse_raw_csv_text(csv_text)

    assert len(rows) == 2
    assert rows[0] == {
        "name": "Alice",
        "email": "alice@example.com",
        "company": "Acme Corp",
        "city": "NYC",
        "notes": "Lead"
    }
    assert rows[1]["name"] == "Bob"


# ==========================================
# 2. DIRTY & EMPTY ROW HANDLING
# ==========================================

def test_csv_parser_filters_various_empty_rows():
    """Ensures empty lines, whitespace-only lines, and tabbed lines are skipped."""
    csv_text = (
        "name,email,company,city,notes\n"
        "Alice,alice@example.com,Acme Corp,NYC,Lead\n"
        ",,,,\n"                        # Pure empty row
        "   ,   ,   ,   ,   \n"        # Spaces-only row
        "\t,\t,\t,\t,\t\n"              # Tabs-only row
        "Bob,bob@example.com,Beta Inc,LA,Customer\n"
    )
    rows = parse_raw_csv_text(csv_text)

    assert len(rows) == 2
    assert rows[0]["name"] == "Alice"
    assert rows[1]["name"] == "Bob"


def test_csv_parser_empty_file_returns_empty_list():
    """Completely empty file (0 bytes) returns an empty list without throwing an error."""
    rows = parse_raw_csv_text("")
    assert rows == []


def test_csv_parser_header_only_returns_empty_list():
    """File with headers but no records yields 0 parsed rows."""
    csv_text = "name,email,company,city,notes\n"
    rows = parse_raw_csv_text(csv_text)
    assert rows == []


# ==========================================
# 3. QUOTES, COMMAS & FORMATTING EDGE CASES
# ==========================================

def test_csv_parser_handles_quoted_commas_and_newlines():
    """Properly parses fields containing embedded commas or internal newlines inside quotes."""
    csv_text = (
        'name,email,company,city,notes\n'
        '"Doe, Jane",jane@example.com,"Acme, Inc.",Austin,"Line 1\nLine 2"\n'
    )
    rows = parse_raw_csv_text(csv_text)

    assert len(rows) == 1
    assert rows[0]["name"] == "Doe, Jane"
    assert rows[0]["company"] == "Acme, Inc."
    assert rows[0]["notes"] == "Line 1\nLine 2"


def test_csv_parser_supports_windows_and_mac_line_endings():
    """Ensures Windows (CRLF) and Linux/Mac (LF) line endings parse identically."""
    windows_csv = "name,email,company,city,notes\r\nAlice,a@ex.com,Acme,NYC,Note1\r\n"
    linux_csv = "name,email,company,city,notes\nAlice,a@ex.com,Acme,NYC,Note1\n"

    assert parse_raw_csv_text(windows_csv) == parse_raw_csv_text(linux_csv)


# ==========================================
# 4. MISALIGNED & UNEXPECTED HEADERS
# ==========================================

def test_csv_parser_handles_missing_columns_in_header():
    """If the CSV is missing expected header columns, .get() safely defaults to empty strings."""
    csv_text = (
        "name,email\n"
        "Charlie,charlie@example.com\n"
    )
    rows = parse_raw_csv_text(csv_text)

    assert len(rows) == 1
    assert rows[0]["name"] == "Charlie"
    assert rows[0]["email"] == "charlie@example.com"
    assert rows[0]["company"] == ""
    assert rows[0]["city"] == ""
    assert rows[0]["notes"] == ""


def test_csv_parser_handles_extra_unrecognized_columns():
    """Extra unexpected CSV headers are safely ignored by your key mapping."""
    csv_text = (
        "name,email,company,city,notes,extra_col1,extra_col2\n"
        "Dave,dave@example.com,DataCo,Chicago,Note,UnusedValue1,UnusedValue2\n"
    )
    rows = parse_raw_csv_text(csv_text)

    assert len(rows) == 1
    assert "extra_col1" not in rows[0]
    assert rows[0]["name"] == "Dave"


def test_csv_parser_handles_malformed_short_rows():
    """Rows with fewer values than headers assign None or empty strings safely."""
    csv_text = (
        "name,email,company,city,notes\n"
        "Eve,eve@example.com\n"  # Missing company, city, notes
    )
    rows = parse_raw_csv_text(csv_text)

    assert len(rows) == 1
    assert rows[0]["name"] == "Eve"
    assert rows[0]["company"] == "" or rows[0]["company"] is None