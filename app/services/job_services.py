import uuid
from datetime import datetime, timezone

# Responsible for updating the db so the frontend knows what's happening
# connects frontend to backend
def create_job(workspace_id: str) -> dict:
    job_id = f"job_{uuid.uuid4().hex[:8]}"
    created_at = datetime.now(timezone.utc).isoformat()

    new_job = {
        "job_id": job_id,
        "workspace_id": workspace_id.strip(),
        "status": "pending",
        "total_records": 0,
        "error_message": None,
        "created_at": created_at,
        "started_at": None,
        "completed_at": None
    }

    print("\n"+"="*40)
    print("STORAGE EVENT: TEMPORARY PRINT OUT")
    print(f"Successfully Created New Job:")
    print(f" - Job ID: {new_job['job_id']}")
    print(f" - Workspace ID: {new_job['workspace_id']}")
    print(f" - Status: {new_job['status']}")
    print(f" - Total Records Processed: {new_job['total_records']}")
    print(f" - Error Message: {new_job['error_message']}")
    print(f" - Created At: {new_job['created_at']}")
    print(f" - Started At: {new_job['started_at']}")
    print(f" - Completed At: {new_job['completed_at']}")
    print("="*40 + "\n")

    return new_job

def get_job_status(job_id: str) -> dict:
    print("\n"+"="*40)
    print(f"STORAGE EVENT: TEMPORARY PRINT OUT")
    print(f"Fetching Status for Job ID: {job_id.strip()}")
    print("="*40 + "\n")
    return {
        "job_id": job_id.strip(),
        "status": "completed", #hardcoded, will be fixed in part 2
        "total_records": 0,
        "error_message": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": datetime.now(timezone.utc).isoformat()
    }