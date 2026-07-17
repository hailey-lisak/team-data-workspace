import uuid
from datetime import datetime, timezone
from sqlmodel import select, Session
from database.models import Workspace, create_workspace_db, get_workspace_db, update_workspace_db, delete_workspace_db

def create_workspace(db, name: str, user_id: str) -> dict:
    workspace_id = f"wsp_{uuid.uuid4().hex[:8]}"
    created_at = datetime.now(timezone.utc).isoformat()

    new_workspace = {
        "workspace_id": workspace_id,
        "name": name.strip(),
        "user_id": user_id.strip(),
        "created_at": created_at
    }

    """ print("\n"+"="*40)
    print("STORAGE EVENT: TEMPORARY PRINT OUT")
    print(f"Successfully Created Workspace:")
    print(f" - User ID: {new_workspace['user_id']}")
    print(f" - Name: {new_workspace['name']}")
    print(f" - Workspace ID : {new_workspace['workspace_id']}")
    print(f" - Created At: {new_workspace['created_at']}")
    print("="*40 + "\n") """
    db_record = create_workspace_db(session=db, workspace_data=new_workspace)

    return new_workspace
def get_all_workspaces(db: Session) -> list:
    """
    Fetches all workspaces from the database.
    """
    workspaces = db.exec(select(Workspace)).all()
    formatted_workspaces = []
    
    for ws in workspaces:
        if hasattr(ws, "model_dump"):
            formatted_workspaces.append(ws.model_dump())
        elif hasattr(ws, "dict"):
            formatted_workspaces.append(ws.dict())
        else:
            formatted_workspaces.append({
                "workspace_id": ws.workspace_id,
                "name": ws.name,
                "user_id": ws.user_id,
                "created_at": ws.created_at.isoformat() if ws.created_at else None
            })
    return formatted_workspaces

def update_workspace(db: Session, workspace_id: str, new_name: str) -> dict | None:
    """
    Validates and updates an existing workspace's details.
    """
    # Call your ORM update function directly
    updated_ws = update_workspace_db(session=db, workspace_id=workspace_id, new_name=new_name)
    if not updated_ws:
        return None
        
    return {
        "workspace_id": updated_ws.workspace_id,
        "name": updated_ws.name,
        "user_id": updated_ws.user_id,
        "created_at": updated_ws.created_at.isoformat() if updated_ws.created_at else None
    }

def delete_workspace(db: Session, workspace_id: str) -> bool:
    """
    Removes a workspace completely.
    """
    return delete_workspace_db(session=db, workspace_id=workspace_id)