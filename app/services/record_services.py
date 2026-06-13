import uuid
from datetime import datetime, timezone
from pydantic import EmailStr

def create_record(workspace_id: str, name: str, email: EmailStr, company: str, city: str, notes: str = "") -> dict:
    '''should every id be truncated to 8 characters?'''
    record_id = f"rec_{uuid.uuid4().hex[:8]}"
    created_at = datetime.now(timezone.utc).isoformat()

    name_clean = name.strip() if name else ""
    email_clean = email.strip().lower() if email else ""
    company_clean = company.strip() if company else ""
    city_clean = city.strip() if city else ""
    notes_clean = notes.strip() if notes else ""

    is_valid = bool(email_clean)

    if not email_clean and not company_clean:
        tag = "incomplete"
    elif not email_clean:
        tag = "missing_email"
    elif not company_clean:
        tag = "missing_company"
    else:
        tag = "complete"    
    
    processed_at = datetime.now(timezone.utc).isoformat()

    new_record = {
        "record_id": record_id,
        "workspace_id": workspace_id,
        "name": name_clean,
        "email": email_clean,
        "company": company_clean,
        "city": city_clean,
        "notes": notes_clean,
        "is_valid": is_valid,
        "tag": tag,
        "created_at": created_at,
        "processed_at": processed_at
    }
    print("\n"+"="*40)
    print("STORAGE EVENT: TEMPORARY PRINT OUT")
    print(f"Successfully Creted New Record:")
    print(f" - Record ID: {new_record['record_id']}")
    print(f" - Workspace ID: {new_record['workspace_id']}")
    print(f" - Name: {new_record['name']}")     
    print(f" - Email: {new_record['email']}")
    print(f" - Company: {new_record['company']}")
    print(f" - City: {new_record['city']}")
    print(f" - Notes: {new_record['notes']}")
    print(f" - Status: {new_record['is_valid']}")
    print(f" - Tag Assigned: {new_record['tag']}")
    print(f" - Created At: {new_record['created_at']}")
    print(f" - Processed At: {new_record['processed_at']}")
    print("="*40 + "\n")

    return new_record