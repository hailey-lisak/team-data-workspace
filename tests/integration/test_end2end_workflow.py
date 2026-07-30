import os
import uuid
import requests

# Dynamically pick up container URL or fallback to localhost
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def test_complete_data_workspace_e2e_pipeline():
    print("\n" + "=" * 60)
    print("STARTING E2E WORKFLOW TEST")
    print("=" * 60)

    unique_suffix = uuid.uuid4().hex[:6]
    created_user_id = None
    created_workspace_id = None

    try:
        # -------------------------------------------------------------
        # STEP 1: CREATE A NEW USER
        # -------------------------------------------------------------
        user_payload = {
            "email": f"analyst_{unique_suffix}@company.com",
            "name": "Data Analyst",
        }
        print(f"\n[Step 1] Creating User: {user_payload['email']}")
        user_res = requests.post(f"{BASE_URL}/users/", json=user_payload)
        assert user_res.status_code in (200, 201), f"User creation failed: {user_res.text}"

        user_data = user_res.json()
        created_user_id = user_data.get("user_id") or user_data.get("id")
        print(f"  ✓ User created with ID: {created_user_id}")

        # -------------------------------------------------------------
        # STEP 2: CREATE A WORKSPACE FOR THE USER
        # -------------------------------------------------------------
        ws_payload = {
            "name": f"Analytics_Workspace_{unique_suffix}",
            "user_id": created_user_id,
        }
        print(f"\n[Step 2] Creating Workspace: {ws_payload['name']}")
        ws_res = requests.post(f"{BASE_URL}/workspaces", json=ws_payload)
        assert ws_res.status_code in (200, 201), f"Workspace creation failed: {ws_res.text}"

        ws_data = ws_res.json()
        created_workspace_id = ws_data.get("workspace_id") or ws_data.get("id")
        print(f"  ✓ Workspace created with ID: {created_workspace_id}")

        # -------------------------------------------------------------
        # STEP 3: IMPORT RECORDS VIA CSV UPLOAD
        # Hits: POST /workspaces/{workspace_id}/records/import
        # -------------------------------------------------------------
        print(f"\n[Step 3] Uploading CSV records into Workspace {created_workspace_id}...")
        
        csv_content = (
            "name,email,company,city,notes\n"
            f"Alice Smith,alice_{unique_suffix}@example.com,Acme Corp,New York,VIP Client\n"
            f"Bob Jones,bob_{unique_suffix}@example.com,Tech Inc,San Francisco,Standard User\n"
        )
        
        files = {
            "file": ("records.csv", csv_content, "text/csv")
        }
        
        # Path parameter URL: /workspaces/{created_workspace_id}/records/import
        rec_res = requests.post(
            f"{BASE_URL}/workspaces/{created_workspace_id}/records/import",
            files=files,
        )
        assert rec_res.status_code in (200, 201), f"CSV Import failed: {rec_res.text}"
        
        import_summary = rec_res.json()
        print(f"  ✓ CSV imported successfully! Response: {import_summary}")

        # -------------------------------------------------------------
        # STEP 4: TRIGGER A PROCESSING JOB FOR THE WORKSPACE
        # -------------------------------------------------------------
        job_payload = {"workspace_id": created_workspace_id}
        print(f"\n[Step 4] Triggering job for Workspace {created_workspace_id}...")
        job_res = requests.post(
            f"{BASE_URL}/workspaces/{created_workspace_id}/jobs",
            json=job_payload,
        )
        assert job_res.status_code in (200, 201), f"Job creation failed: {job_res.text}"

        job_data = job_res.json()
        created_job_id = (
            job_data.get("job_id")
            or job_data.get("id")
            or job_data.get("uuid")
        )
        print(f"  ✓ Job queued with ID: {created_job_id}")

        # -------------------------------------------------------------
        # STEP 5: UPDATE JOB STATUS TO COMPLETED
        # -------------------------------------------------------------
        update_job_payload = {
            "status": "completed",
            "total_records": import_summary.get("count", 2),
            "error_message": "",
        }
        print(f"\n[Step 5] Transitioning Job {created_job_id} -> COMPLETED")
        update_res = requests.put(
            f"{BASE_URL}/workspaces/{created_workspace_id}/jobs/{created_job_id}",
            json=update_job_payload,
        )
        assert update_res.status_code == 200, f"Job status update failed: {update_res.text}"

        final_job = update_res.json()
        assert final_job.get("status") == "completed"
        print("  ✓ Job status transitioned to COMPLETED successfully")

        print("\n" + "=" * 60)
        print("E2E WORKFLOW TEST PASSED GREEN!")
        print("=" * 60)

    finally:
        # -------------------------------------------------------------
        # STEP 6: CLEANUP RESOURCES
        # -------------------------------------------------------------
        print("\n[Step 6] Running Teardown/Cleanup...")
        if created_workspace_id:
            del_ws = requests.delete(f"{BASE_URL}/workspaces/{created_workspace_id}")
            print(f"  ✓ Deleted Workspace {created_workspace_id} (Status: {del_ws.status_code})")
        if created_user_id:
            del_usr = requests.delete(f"{BASE_URL}/users/{created_user_id}")
            print(f"  ✓ Deleted User {created_user_id} (Status: {del_usr.status_code})")


if __name__ == "__main__":
    test_complete_data_workspace_e2e_pipeline()