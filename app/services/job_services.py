import uuid
from datetime import datetime, timezone
from sqlmodel import Session
from database.models import Job

def create_job(db: Session, workspace_id: str) -> dict:
    """
    Initializes a background processing job for a workspace.
    """
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    created_at_dt = datetime.now(timezone.utc)

    db_job = Job(
        job_id=job_id,
        workspace_id=workspace_id.strip(),
        status="pending",
        total_records=0,
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