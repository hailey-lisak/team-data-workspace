from fastapi import FastAPI
from app.api import users, workspaces, records, jobs

'''
Initializes a new FastAPI web application
This automatically builds my interactive Swagger documentation configuration page
    - Swagger File: blueprint file that describes how the web API works in JSON or YAML
'''
app = FastAPI(
    title="Team Data Workspace API",
    version = "1.0.0",
    description = "PArt 1 Implementation"
)

'''
app.include_router(): takes the isolated department files and plugs them into the main system
    - also defines the URL architecture 
'''
app.include_router(users.router, tags=["Users"])
app.include_router(workspaces.router, tags=["Workspaces"])


app.include_router(records.router, prefix="/workspaces/{workspace_id}", tags=["Records"])
app.include_router(jobs.router, prefix="/workspaces/{workspace_id}", tags=["Jobs"])

@app.get("/")
def read_root():
    return {"message": "Team Data Workspace API is functional."}