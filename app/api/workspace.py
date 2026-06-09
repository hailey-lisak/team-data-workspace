from fastapi import APIRouter, status 
from pydantic import BaseModel
from app.services import workspace_services

router = APIRouter()

class WorkspaceCreateRequest(BaseModel):
    name: str
    user_id: str

@router.post("/workspace", status_code=status.HTTP_201_CREATED)
def create_workspace(payload: WorkspaceCreateRequest):
    saved_workspace = workspace_services.create_workspace(
        name = payload.name,
        user_id = payload.user_id,
    )
    return saved_workspace