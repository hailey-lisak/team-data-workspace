from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr
from app.services import record_services

router = APIRouter()

class RecordCreateRequest(BaseModel):
    workspace_id: str
    name: str
    email: EmailStr
    company: str
    city: str
    notes: str

@router.post("/records", status_code=status.HTTP_201_CREATED)
def create_record(payload: RecordCreateRequest):
    saved_record = record_services.create_record(
        workspace_id = payload.workspace_id,
        name = payload.name,
        email = payload.email,
        company = payload.company,
        city = payload.city,
        notes = payload.notes
    )
    return saved_record