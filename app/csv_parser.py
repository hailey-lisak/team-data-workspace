# app/csv_parser.py
import csv
from io import StringIO
from typing import Any, Dict, List, Tuple
from pydantic import ValidationError

from app.schemas import RecordIngestRow


def parse_and_validate_csv_stream(
    file_contents: str,
) -> Tuple[List[RecordIngestRow], List[Dict[str, Any]]]:
    """
    Parses a string of CSV content, validates each row against RecordIngestRow,
    and returns a tuple containing valid schema instances and detailed error logs.
    """
    valid_records: List[RecordIngestRow] = []
    errors: List[Dict[str, Any]] = []

    # StringIO allows csv.DictReader to process text streams in memory
    stream = StringIO(file_contents)
    reader = csv.DictReader(stream)

    for row_idx, row in enumerate(reader, start=1):
        try:
            validated_row = RecordIngestRow(**row)
            valid_records.append(validated_row)
        except ValidationError as e:
            errors.append(
                {
                    "row": row_idx,
                    "raw_data": row,
                    "details": e.errors(),
                }
            )

    return valid_records, errors