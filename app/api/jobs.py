from fastapi import APIRouter, status
from pydantic import BaseModel
from app.services import job_services

router = APIRouter()

class JobCreateRequest(BaseModel):
    workspace_id: str
    
@router.post("/jobs", status_code=status.HTTP_201_CREATED)
def create_job(payload: JobCreateRequest):
    saved_job = job_services.create_job(
        workspace_id = payload.workspace_id,
    )
    return saved_job