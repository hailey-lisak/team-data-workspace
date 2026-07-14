from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, Session, select
# edis to orm to call service to ccall orm to then create a rec ord in db
# update docker compose to include the SQL alchemy upgrades to docker then push and reploy docker
#then use curl command
#its running on the server
#send email about progress on friday
#get test file done, integrate and get recorfd inserted and test tfiels shoudl rfun and be able tgo show the recorfd persisted for insert inset inster get get get
#implement sql alcehmy in orm and integrate the call with services and use syncrhonous calls then asynchronous alchemy calls
#read about synch and async and get everything integreated and have eveerything deployed as a container, be able to run a query
# ==========================================
# 1. THE USER ORM MODEL
# use orm and its methods to actually do crud operations
# explame, users defined by class for users and those should have a 1 on 1 relationship on what i have in database like creating record method/functions in class and then that internally will habve logic that will allow me to have logic in the db by calling
# scrfipt used run to create a database based on the logic. orm is a part of application package it jst helps keep db secure and genertea a relational structure by using onjects to tie back to service
# so api calls servicde, service takes app from api http request then maps it back to specific objects in orm. then based on what im trying to do , its going tocall a create function
# cretae function does the magic to connect to data

# script is sequal database
# orm is application specific; the way the app will communicate to the database
# getting info from user than printing it; 
# start with create -> start with users "create an orm for the user table and i should be able to create update and delete a user file"
# ==========================================
class User(SQLModel, table=True):
    __tablename__: str = "users"  # Links directly to your 'users' table

    #user_id: str = Field(primary_key=True)
    user_id: Optional[str] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    email: str = Field(max_length=255, unique=True, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship: Allows Python to easily fetch a user's workspaces
    # e.g., current_user.workspaces
    workspaces: list["Workspace"] = Relationship(back_populates="user")
# User CRUD actions
# ─── CREATE ───────────────────────────────────────────────────────────
def create_user_db(session: Session, user_data: dict) -> User:
    """Takes your processed service dictionary, maps it to your exact ORM parameters, 
    and saves it permanently to Postgres.
    """
    db_user = User(
        user_id=user_data["user_id"],
        name=user_data["name"],
        email=user_data["email"],
        # Convert your ISO string back into a datetime object for the database
        created_at=datetime.fromisoformat(user_data["created_at"])
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

# ─── READ (Helper) ────────────────────────────────────────────────────
def get_user_db(session: Session, user_id: str) -> Optional[User]:
    """Finds a user by their unique user_id."""
    statement = select(User).where(User.user_id == user_id)
    return session.exec(statement).first()

# ─── UPDATE ───────────────────────────────────────────────────────────
def update_user_db(session: Session, user_id: str, new_name: str) -> Optional[User]:
    """Updates a user's name while respecting your max_length=100 constraint."""
    db_user = get_user_db(session, user_id)
    if db_user:
        db_user.name = new_name.strip()[:100]  # Enforce your max length parameter
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user

# ─── DELETE ───────────────────────────────────────────────────────────
def delete_user_db(session: Session, user_id: str) -> bool:
    """Deletes a user from the database completely. Returns True if successful."""
    db_user = get_user_db(session, user_id)
    if not db_user:
        return False
    session.delete(db_user)
    session.commit()
    return True

# ==========================================
# 2. THE WORKSPACE ORM MODEL
# ==========================================
class Workspace(SQLModel, table=True):
    __tablename__: str = "workspaces"

    workspace_id: str = Field(primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Foreign key links back to your users table
    user_id: str = Field(foreign_key="users.user_id", nullable=False)

    # Relationships
    user: User = Relationship(back_populates="workspaces")
    records: List["Record"] = Relationship(back_populates="workspace")
    jobs: List["Job"] = Relationship(back_populates="workspace")

# Workspace Database Actions
def create_workspace_db(session: Session, workspace_data: dict) -> Workspace:
    db_workspace = Workspace(
        workspace_id=workspace_data["workspace_id"],
        name=workspace_data["name"],
        user_id=workspace_data["user_id"],
        created_at=datetime.fromisoformat(workspace_data["created_at"])
    )
    session.add(db_workspace)
    session.commit()
    session.refresh(db_workspace)
    return db_workspace

def get_workspace_db(session: Session, workspace_id: str) -> Optional[Workspace]:
    statement = select(Workspace).where(Workspace.workspace_id == workspace_id)
    return session.exec(statement).first()

def update_workspace_db(session: Session, workspace_id: str, new_name: str) -> Optional[Workspace]:
    db_workspace = get_workspace_db(session, workspace_id)
    if db_workspace:
        db_workspace.name = new_name.strip()[:100]
        session.add(db_workspace)
        session.commit()
        session.refresh(db_workspace)
    return db_workspace

def delete_workspace_db(session: Session, workspace_id: str) -> bool:
    db_workspace = get_workspace_db(session, workspace_id)
    if not db_workspace:
        return False
    session.delete(db_workspace)
    session.commit()
    return True


# ==========================================
# 3. THE RECORD ORM MODEL
# ==========================================
class Record(SQLModel, table=True):
    __tablename__: str = "records"

    record_id: str = Field(primary_key=True)
    raw_data: str = Field(nullable=False)  # Your data payload string
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Foreign key links back to your workspaces table
    workspace_id: str = Field(foreign_key="workspaces.workspace_id", nullable=False)

    # Relationship back to its workspace parent
    workspace: Workspace = Relationship(back_populates="records")

# Record Database Actions
def create_record_db(session: Session, record_data: dict) -> Record:
    db_record = Record(
        record_id=record_data["record_id"],
        raw_data=record_data["raw_data"],
        workspace_id=record_data["workspace_id"],
        created_at=datetime.fromisoformat(record_data["created_at"])
    )
    session.add(db_record)
    session.commit()
    session.refresh(db_record)
    return db_record

def get_record_db(session: Session, record_id: str) -> Optional[Record]:
    statement = select(Record).where(Record.record_id == record_id)
    return session.exec(statement).first()

def delete_record_db(session: Session, record_id: str) -> bool:
    db_record = get_record_db(session, record_id)
    if not db_record:
        return False
    session.delete(db_record)
    session.commit()
    return True


# ==========================================
# 4. THE JOB ORM MODEL
# ==========================================
class Job(SQLModel, table=True):
    __tablename__: str = "jobs"

    job_id: str = Field(primary_key=True)
    task_type: str = Field(max_length=50, nullable=False)
    status: str = Field(max_length=20, default="pending", nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # Foreign key links back to your workspaces table
    workspace_id: str = Field(foreign_key="workspaces.workspace_id", nullable=False)

    # Relationship back to its workspace parent
    workspace: Workspace = Relationship(back_populates="jobs")

# Job Database Actions
def create_job_db(session: Session, job_data: dict) -> Job:
    db_job = Job(
        job_id=job_data["job_id"],
        task_type=job_data["task_type"],
        status=job_data.get("status", "pending"),
        workspace_id=job_data["workspace_id"],
        created_at=datetime.fromisoformat(job_data["created_at"])
    )
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job

def get_job_db(session: Session, job_id: str) -> Optional[Job]:
    statement = select(Job).where(Job.job_id == job_id)
    return session.exec(statement).first()

def update_job_status_db(session: Session, job_id: str, new_status: str) -> Optional[Job]:
    db_job = get_job_db(session, job_id)
    if db_job:
        db_job.status = new_status.strip()[:20]
        session.add(db_job)
        session.commit()
        session.refresh(db_job)
    return db_job