import uuid
from datetime import datetime, timezone
from sqlmodel import Session
from database.models import Job, Record
from sqlmodel import select, func
import time


def create_job(db: Session, workspace_id: str) -> dict:
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    created_at_dt = datetime.now(timezone.utc)

    # THIS IS THE MAGIC LINE - Ensure this is in your file!
    record_count_query = select(func.count(Record.record_id)).where(Record.workspace_id == workspace_id.strip())
    existing_records_count = db.exec(record_count_query).one()

    db_job = Job(
        job_id=job_id,
        workspace_id=workspace_id.strip(),
        status="pending",
        total_records=existing_records_count,  # Uses the dynamic count!
        error_message=None,
        created_at=created_at_dt,
        started_at=None,
        completed_at=None
    )
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)

    return {
        "job_id": db_job.job_id,
        "workspace_id": db_job.workspace_id,
        "status": db_job.status,
        "total_records": db_job.total_records,
        "error_message": db_job.error_message,
        "created_at": db_job.created_at.isoformat(),
        "started_at": None,
        "completed_at": None
    }

def get_job_status(db: Session, job_id: str) -> dict | None:
    """
    Fetches the processing details of a background job.
    """
    db_job = db.get(Job, job_id)
    if not db_job:
        return None
        
    return {
        "job_id": db_job.job_id,
        "workspace_id": db_job.workspace_id,
        "status": db_job.status,
        "total_records": db_job.total_records,
        "error_message": db_job.error_message,
        "created_at": db_job.created_at.isoformat() if db_job.created_at else None,
        "started_at": db_job.started_at.isoformat() if db_job.started_at else None,
        "completed_at": db_job.completed_at.isoformat() if db_job.completed_at else None
    }

def update_job_status(db: Session, job_id: str, new_status: str, total_records: int = 0, error_message: str = None) -> dict | None:
    """
    Updates operational metrics and transitions timestamps based on execution state.
    """
    db_job = db.get(Job, job_id)
    if not db_job:
        return None
        
    db_job.status = new_status.strip()[:20]
    db_job.total_records = total_records
    db_job.error_message = error_message
    
    # Smart transitions for tracking engine progress
    if new_status.lower() == "running" and not db_job.started_at:
        db_job.started_at = datetime.now(timezone.utc)
    elif new_status.lower() in ["completed", "failed"] and not db_job.completed_at:
        db_job.completed_at = datetime.now(timezone.utc)
        
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    
    return get_job_status(db, job_id)

def process_workspace_data_worker(db: Session, job_id: str, workspace_id: str):
    """
    Background worker that fetches, cleans, validates, and updates records for a workspace.
    """
    # 1. Boot up the job into 'running' state
    update_job_status(db, job_id=job_id, new_status="running")
    
    try:
        # 2. Grab all records for this workspace
        records_query = select(Record).where(Record.workspace_id == workspace_id)
        records = db.exec(records_query).all()
        
        total_processed = 0
        
        for record in records:
            # Simulate heavy data crunching processing time (0.5 seconds per row)
            time.sleep(0.5) 
            
            # --- 3. THE CLEANING & VALIDATION ENGINE ---
            # Clean Name (Title Case: "hailey lisak" -> "Hailey Lisak")
            if record.name:
                record.name = record.name.strip().title()
                
            # Clean City (Title Case: "pittsburgh" -> "Pittsburgh")
            if record.city:
                record.city = record.city.strip().title()
                
            # Clean Email (Lowercase & Validate format)
            if record.email:
                record.email = record.email.strip().lower()
                if "@" in record.email and "." in record.email.split("@")[-1]:
                    record.is_valid = True
                    record.tag = "valid"
                else:
                    record.is_valid = False
                    record.tag = "invalid_email"
            else:
                record.is_valid = False
                record.tag = "missing_email"
                
            # Save the updated record state
            db.add(record)
            total_processed += 1
            
            # Keep the job record count updated dynamically
            db_job = db.get(Job, job_id)
            if db_job:
                db_job.total_records = total_processed
                db.add(db_job)
                db.commit()

        # 4. Success state transition
        update_job_status(db, job_id=job_id, new_status="completed", total_records=total_processed)
        
    except Exception as e:
        # 5. Fail-safe state transition to prevent server crashes
        db.rollback()
        update_job_status(db, job_id=job_id, new_status="failed", error_message=str(e))