import uuid
def create_workspace(name: str, user_id: str) -> dict:
    workspace_id = f"wsp_{uuid.uuid4().hex[:8]}"
    '''
        NEED CREATED_AT
    '''
    new_workspace = {
        "workspace_id": workspace_id,
        "name:": name.strip(),
        "user_id": user_id.strip()
    }

    print("\n"+"="*40)
    print("STORAGE EVENT: TEMPORARY PRINT OUT")
    print(f"Successfully Creted Workspace:")
    print(f" - User ID: {new_workspace['user_id']}")
    print(f" - Name: {new_workspace['name']}")
    print(f" - Workspace ID : {new_workspace['workspace_id']}")
    print("="*40 + "\n")

    return new_workspace
