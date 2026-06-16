from fastapi import FastAPI
from app.api import users, workspaces, records, jobs

app = FastAPI(
    title="Team Data Workspace API",
    version = "1.0.0",
    description = "PArt 1 Implementation"
)

app.include_router(users.router, tags=["Users"])
app.include_router(workspaces.router, tags=["Workspaces"])


app.include_router(records.router, prefix="/workspaces/{workspace_id}", tags=["Records"])
app.include_router(jobs.router, prefix="/workspaces/{workspace_id}", tags=["Jobs"])

@app.get("/")
def read_root():
    return {"message": "Team Data Workspace API is functional."}