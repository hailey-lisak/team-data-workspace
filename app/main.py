# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Imports from your API router modules
from app.api import jobs, records, users, workspaces
from database.connection import create_db_and_tables


# ─── LIFESPAN FUNCTION TO RUN TABLE CREATION ───────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    # This fires up the exact millisecond you run your uvicorn command
    create_db_and_tables()
    yield


# ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="Team Data Workspace API",
    version="1.0.0",
    description="Part 1 Implementation",
    lifespan=lifespan,
)

# ─── ROUTER REGISTRATION ───────────────────────────────────────
app.include_router(users.router, tags=["Users"])
app.include_router(workspaces.router, tags=["Workspaces"])

app.include_router(
    records.router, prefix="/workspaces/{workspace_id}", tags=["Records"]
)
app.include_router(
    jobs.router, prefix="/workspaces/{workspace_id}", tags=["Jobs"]
)


# ─── UTILITY ROUTES ───────────────────────────────────────────
@app.get("/")
def read_root():
    return {"message": "Team Data Workspace API is functional."}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}