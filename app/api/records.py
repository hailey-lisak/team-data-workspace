from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr
from app.services import record_services

router = APIRouter()

class RecordCreateRequest(BaseModel):
    #workspace_id will come from the URL path
    name: str
    email: EmailStr
    company: str
    city: str
    notes: str

@router.post("/records/import", status_code=status.HTTP_201_CREATED)
def import_record(workspace_id: str, payload:RecordCreateRequest):
    saved_record = record_services.create_record(
        workspace_id = workspace_id,
        name = payload.name,
        email = payload.email,
        company = payload.company,
        city = payload.city,
        notes = payload.notes
    )
    return saved_record