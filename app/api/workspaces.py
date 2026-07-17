from fastapi import APIRouter, status, HTTPException 
from pydantic import BaseModel
from app.services import workspace_services
from sqlmodel import Session
from database.connection import engine  # <-- Make sure engine is imported!

router = APIRouter()

class WorkspaceCreateRequest(BaseModel):
    name: str
    user_id: str
# Schema for updating workspace details
class WorkspaceUpdateRequest(BaseModel):
    name: str

@router.post("/workspaces", status_code=status.HTTP_201_CREATED)
def create_workspace(payload: WorkspaceCreateRequest):
    # 1. Open the database session
    with Session(engine) as session:
        # 2. Pass the session ('db') into your service
        saved_workspace = workspace_services.create_workspace(
            name=payload.name,
            user_id=payload.user_id,
            db=session  # <--- This supplies the missing session!
        )
    # 3. Return the saved workspace dictionary
    return saved_workspace

# ─── 1. GET ALL WORKSPACES ──────────────────────────────────────────
@router.get("/workspaces")
def get_workspaces_endpoint():
    """
    Fetches and returns all workspaces.
    """
    with Session(engine) as session:
        return workspace_services.get_all_workspaces(db=session)

# ─── 2. UPDATE WORKSPACE ────────────────────────────────────────────
@router.put("/workspaces/{workspace_id}")
def update_workspace_endpoint(workspace_id: str, payload: WorkspaceUpdateRequest):
    """
    Updates the name of a specific workspace.
    """
    with Session(engine) as session:
        updated_ws = workspace_services.update_workspace(
            db=session,
            workspace_id=workspace_id,
            new_name=payload.name
        )
        if not updated_ws:
            raise HTTPException(status_code=404, detail="Workspace not found")
        return updated_ws

# ─── 3. DELETE WORKSPACE ────────────────────────────────────────────
@router.delete("/workspaces/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workspace_endpoint(workspace_id: str):
    """
    Permanently deletes a workspace by its unique ID.
    """
    with Session(engine) as session:
        success = workspace_services.delete_workspace(db=session, workspace_id=workspace_id)
        if not success:
            raise HTTPException(status_code=404, detail="Workspace not found")
        return None