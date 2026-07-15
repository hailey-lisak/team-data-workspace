from sqlmodel import create_engine, SQLModel
from database.models import User, Workspace, Record, Job
import os
# 1. Replace this with your actual local PostgreSQL connection string
# will have to use haileylisak:[password] when running postgre via Docker
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:password123@db:5432/postgres"

# 2. The engine is the connection pool manager that talks to port 5432
engine = create_engine(DATABASE_URL, echo=True) 
# Setting echo=True makes SQLModel print the raw SQL to your terminal so you can see it work!

# 3. This is the function that physically builds the empty grids/tables in Postgres
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)