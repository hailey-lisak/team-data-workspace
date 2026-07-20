from pydantic import BaseModel
from app.services import record_services
from sqlmodel import Session
from database.connection import engine
from database.models import Record, Workspace
from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends
import io
import csv
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

# CSV Upload Endpoint
@router.post("/records/import", status_code=status.HTTP_201_CREATED)
def import_records_csv(workspace_id: str, file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV.")

    contents = file.file.read().decode("utf-8")
    buffer = io.StringIO(contents)
    reader = csv.DictReader(buffer)

    created_records = []
    with Session(engine) as session:
        for row in reader:
            # Skip completely empty rows
            #if not any(row.values()):
            #    continue
            if not any(val and val.strip() for val in row.values()):
                continue

            record = record_services.create_record(
                db=session,
                workspace_id=workspace_id,
                name=row.get("name", ""),
                email=row.get("email", ""),
                company=row.get("company", ""),
                city=row.get("city", ""),
                notes=row.get("notes", "")
            )
            created_records.append(record)

    return {
        "message": "CSV imported successfully!",
        "count": len(created_records)
    }
