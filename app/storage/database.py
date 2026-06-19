from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Tells Python exactly where the database is in my computer
# Provides the keys (postgres and password) required to access it
# Postgres: open-source Relational Database Management System
#      - Relational: organizes data into strict tables that can link to one another
DATABASE_URL = "postgresql://postgres:password@localhost:5432/workspace_db"

# Like a translator using the SQLAlchemy 
# because PostgresSQL speaks SQL, Python speaks Python.
# Opens and manages the actual network connection between the Python code
# and the Docker container running in the background
engine = create_engine(DATABASE_URL)

# creates temporary and secure scratchpads (sessions) where I can stage my changes,
# make sure it looks right, and then "save" all of these changes at once
# autocommit=False: don't save automatically. db doesn't save changes until we hit db,commit() in our Python code
# autoflush=False: don't push drafts automattically; "flushing" means sending your pending Python data changes 
#                   over the network to the db container, but not permanently saving them yet.
#                   It prevents unnecessary background network chatter between FastAPI and Docker container while still
#                   assembling data objects in memory.
# bind=engine: links this session factory directly to the specific db network engine we created on the line above it
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 
Base = declarative_base()

# Helper function specifically for FastAPI
# Every time a user interacts with my API (like create worksapce)
# this function with automatically:
#      1. open a clean session line to the db
#      2. Hand it to my API endpoint to do its work
#      3. and close the db when the request is done, even if the code crashes
#               (prevents db from runnin out of memory from abandonded connections) 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()