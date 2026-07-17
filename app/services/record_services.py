import uuid
from datetime import datetime, timezone
from sqlmodel import Session
from database.models import Record
from sqlalchemy.orm import Session


def create_record(db: Session, workspace_id: str, name: str, email: str, company: str, city: str, notes: str = "") -> dict:
    record_id = f"rec_{uuid.uuid4().hex[:8]}"
    created_at_dt = datetime.now(timezone.utc)

    # 1. Your original Data Cleansing Engine
    name_clean = name.strip() if name else ""
    email_clean = email.strip().lower() if email else ""
    company_clean = company.strip() if company else ""
    city_clean = city.strip() if city else ""
    notes_clean = notes.strip() if notes else ""

    is_valid = bool(email_clean)

    # 2. Your original Categorization Rules
    if not email_clean and not company_clean:
        tag = "incomplete"
    elif not email_clean:
        tag = "missing_email"
    elif not company_clean:
        tag = "missing_company"
    else:
        tag = "complete"    
    
    processed_at_dt = datetime.now(timezone.utc)

    # 3. Direct SQLModel mapping
    db_record = Record(
        record_id=record_id,
        workspace_id=workspace_id,
        name=name_clean,
        email=email_clean,
        company=company_clean,
        city=city_clean,
        notes=notes_clean,
        is_valid=is_valid,
        tag=tag,
        created_at=created_at_dt,
        processed_at=processed_at_dt
    )
    
    db.add(db_record)
    db.commit()
    db.refresh(db_record)

    # Return the dictionary exactly as Part 1 expected
    return {
        "record_id": db_record.record_id,
        "workspace_id": db_record.workspace_id,
        "name": db_record.name,
        "email": db_record.email,
        "company": db_record.company,
        "city": db_record.city,
        "notes": db_record.notes,
        "is_valid": db_record.is_valid,
        "tag": db_record.tag,
        "created_at": db_record.created_at.isoformat(),
        "processed_at": db_record.processed_at.isoformat()
    }

def get_record(db: Session, record_id: str) -> dict | None:
    db_record = db.get(Record, record_id)
    if not db_record:
        return None
    return {
        "record_id": db_record.record_id,
        "workspace_id": db_record.workspace_id,
        "name": db_record.name,
        "email": db_record.email,
        "company": db_record.company,
        "city": db_record.city,
        "notes": db_record.notes,
        "is_valid": db_record.is_valid,
        "tag": db_record.tag,
        "created_at": db_record.created_at.isoformat(),
        "processed_at": db_record.processed_at.isoformat()
    }

def delete_record(db: Session, record_id: str) -> bool:
    db_record = db.get(Record, record_id)
    if not db_record:
        return False
    db.delete(db_record)
    db.commit()
    return True

