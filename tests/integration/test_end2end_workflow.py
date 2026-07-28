import uuid
import requests

BASE_URL = "http://localhost:8000"


def test_complete_data_workspace_e2e_pipeline():
    print("\n" + "=" * 60)
    print("STARTING E2E USER JOURNEY: User -> Workspace -> Records -> Job")
    print("=" * 60)

    unique_suffix = uuid.uuid4().hex[:6]

    created_user_id = None
    created_workspace_id = None

    try:
        # STEP 1: ONBOARD A NEW USER
        user_payload = {
            "email": f"analyst_{unique_suffix}@company.com",
            "name": "Data Analyst",
        }
        print(f"\n[Step 1] Creating User: {user_payload['email']}")
        user_res = requests.post(f"{BASE_URL}/users/", json=user_payload)
        assert user_res.status_code in (
            200,
            201,
        ), f"User creation failed: {user_res.text}"

        user_data = user_res.json()
        created_user_id = user_data.get("user_id") or user_data.get("id")
        print(f"  ✓ User created successfully with ID: {created_user_id}")

        # STEP 2: USER PROVISION A NEW WORKSPACE
        ws_payload = {
            "name": f"Analytics_Workspace_{unique_suffix}",
            "user_id": created_user_id,
        }
        print(f"\n[Step 2] Provisions Workspace: {ws_payload['name']}")
        ws_res = requests.post(f"{BASE_URL}/workspaces", json=ws_payload)
        assert ws_res.status_code in (
            200,
            201,
        ), f"Workspace creation failed: {ws_res.text}"

        ws_data = ws_res.json()
        created_workspace_id = ws_data.get("workspace_id") or ws_data.get("id")
        print(
            f"  ✓ Workspace provisioned successfully with ID: {created_workspace_id}"
        )

        # STEP 3: INGEST RECORDS INTO WORKSPACE (Updated with required fields)
        print("\n[Step 3] Ingesting batch data records into Workspace...")
        record_ids = []
        sample_records = [
            {
                "workspace_id": created_workspace_id,
                "name": "Alice Smith",
                "email": f"alice_{unique_suffix}@example.com",
                "company": "Acme Corp",
                "city": "New York",
            },
            {
                "workspace_id": created_workspace_id,
                "name": "Bob Jones",
                "email": f"bob_{unique_suffix}@example.com",
                "company": "Tech Inc",
                "city": "San Francisco",
            },
        ]

        for record in sample_records:
            rec_res = requests.post(
                f"{BASE_URL}/workspaces/{created_workspace_id}/records",
                json=record,
            )
            assert rec_res.status_code in (
                200,
                201,
            ), f"Record creation failed: {rec_res.text}"
            rec_id = rec_res.json().get("record_id") or rec_res.json().get("id")
            record_ids.append(rec_id)

        print(f"  ✓ Successfully ingested {len(record_ids)} records")

        # STEP 4: TRIGGER A PROCESSING JOB FOR THE WORKSPACE
        job_payload = {"workspace_id": created_workspace_id}
        print(
            f"\n[Step 4] Triggering batch process job for Workspace {created_workspace_id}"
        )
        job_res = requests.post(
            f"{BASE_URL}/workspaces/{created_workspace_id}/jobs",
            json=job_payload,
        )
        assert job_res.status_code in (
            200,
            201,
        ), f"Job trigger failed: {job_res.text}"

        job_data = job_res.json()
        created_job_id = (
            job_data.get("job_id")
            or job_data.get("id")
            or job_data.get("uuid")
        )
        print(f"  ✓ Processing Job queued with ID: {created_job_id}")

        # STEP 5: SIMULATE JOB COMPLETION & METRICS UPDATE
        update_job_payload = {
            "status": "completed",
            "total_records": len(record_ids),
            "error_message": "",
        }
        print(f"\n[Step 5] Updating status for Job {created_job_id} -> COMPLETED")
        update_res = requests.put(
            f"{BASE_URL}/workspaces/{created_workspace_id}/jobs/{created_job_id}",
            json=update_job_payload,
        )
        assert (
            update_res.status_code == 200
        ), f"Job completion failed: {update_res.text}"

        final_job = update_res.json()
        assert final_job.get("status") == "completed"
        print("  ✓ Job state transitioned to COMPLETED with 0 errors")

        print("\n" + "=" * 60)
        print("E2E PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 60)

    finally:
        # STEP 6: TEARDOWN RESOURCE TREE
        print("\n[Step 6] Cleaning up E2E resources...")
        if created_workspace_id:
            requests.delete(f"{BASE_URL}/workspaces/{created_workspace_id}")
            print(f"  ✓ Cleaned up Workspace: {created_workspace_id}")
        if created_user_id:
            requests.delete(f"{BASE_URL}/users/{created_user_id}")
            print(f"  ✓ Cleaned up User: {created_user_id}")


if __name__ == "__main__":
    test_complete_data_workspace_e2e_pipeline()