import uuid
from datetime import datetime, timezone

def create_workspace(name: str, user_id: str) -> dict:
    workspace_id = f"wsp_{uuid.uuid4().hex[:8]}"
    created_at = datetime.now(timezone.utc).isoformat()

    new_workspace = {
        "workspace_id": workspace_id,
        "name:": name.strip(),
        "user_id": user_id.strip(),
        "created_at": created_at
    }

    print("\n"+"="*40)
    print("STORAGE EVENT: TEMPORARY PRINT OUT")
    print(f"Successfully Creted Workspace:")
    print(f" - User ID: {new_workspace['user_id']}")
    print(f" - Name: {new_workspace['name']}")
    print(f" - Workspace ID : {new_workspace['workspace_id']}")
    print(f" - Created At: {new_workspace['created_at']}")
    print("="*40 + "\n")

    return new_workspace
