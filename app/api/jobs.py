from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services import job_services
from sqlmodel import Session
from database.connection import engine

router = APIRouter()

class JobCreateRequest(BaseModel):
    workspace_id: str

class JobUpdateRequest(BaseModel):
    status: str
    total_records: Optional[int] = 0
    error_message: Optional[str] = None

@router.post("/jobs", status_code=status.HTTP_201_CREATED)
def create_job_endpoint(payload: JobCreateRequest):
    with Session(engine) as session:
        try:
            return job_services.create_job(db=session, workspace_id=payload.workspace_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

@router.get("/jobs/{job_id}")
def get_job_endpoint(job_id: str):
    with Session(engine) as session:
        job = job_services.get_job_status(db=session, job_id=job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

@router.put("/jobs/{job_id}")
def update_job_endpoint(job_id: str, payload: JobUpdateRequest):
    with Session(engine) as session:
        updated_job = job_services.update_job_status(
            db=session,
            job_id=job_id,
            new_status=payload.status,
            total_records=payload.total_records,
            error_message=payload.error_message
        )
        if not updated_job:
            raise HTTPException(status_code=404, detail="Job not found")
        return updated_job