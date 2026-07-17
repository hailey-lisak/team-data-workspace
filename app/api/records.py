from pydantic import BaseModel
from app.services import record_services
from sqlmodel import Session
from database.connection import engine
from database.models import Record, Workspace
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
router = APIRouter()

# Schema matching your engine fields
class RecordCreateRequest(BaseModel):
    workspace_id: str
    name: str
    email: str
    company: str
    city: str
    notes: str = ""

@router.post("/records", status_code=status.HTTP_201_CREATED)
def create_record_endpoint(payload: RecordCreateRequest):
    with Session(engine) as session:
        try:
            return record_services.create_record(
                db=session,
                workspace_id=payload.workspace_id,
                name=payload.name,
                email=payload.email,
                company=payload.company,
                city=payload.city,
                notes=payload.notes
            )
        except Exception:
            raise HTTPException(status_code=400, detail="Ensure the Workspace ID is valid.")

@router.get("/records/{record_id}")
def get_record_endpoint(record_id: str):
    with Session(engine) as session:
        record = record_services.get_record(db=session, record_id=record_id)
        if not record:
            raise HTTPException(status_code=404, detail="Record not found")
        return record

@router.delete("/records/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record_endpoint(record_id: str):
    with Session(engine) as session:
        success = record_services.delete_record(db=session, record_id=record_id)
        if not success:
            raise HTTPException(status_code=404, detail="Record not found")
        return None

