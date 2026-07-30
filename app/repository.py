# app/repository.py
import uuid
from typing import List
from sqlmodel import Session

# Adjust this import to match the location of your models file (e.g., app.database.models or app.models)
from database.models import Record  
from app.schemas import RecordIngestRow


class RecordRepository:
    """Repository layer for performing database operations on Record models."""

    def __init__(self, db_session: Session):
        self.db = db_session

    def bulk_create_records(self, records: List[RecordIngestRow], workspace_id: str) -> int:
        """
        Efficiently converts Pydantic schema rows into SQLModel Record instances
        and bulk inserts them into Postgres for a given workspace.
        """
        if not records:
            return 0

        # Map RecordIngestRow to SQLModel Record instances
        db_records = [
            Record(
                record_id=str(uuid.uuid4()),
                workspace_id=workspace_id,
                name=record.name or "",
                email=record.email or "",
                company=record.company or "",
                city=record.city or "",
                notes=record.notes or "",
                is_valid=True,
                tag="processed",
            )
            for record in records
        ]

        self.db.add_all(db_records)
        self.db.commit()

        return len(db_records)