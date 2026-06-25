from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship

# ==========================================
# 1. THE USER ORM MODEL
# ==========================================
class User(SQLModel, table=True):
    __tablename__: str = "users"  # Links directly to your 'users' table

    user_id: str = Field(primary_key=True, max_length=50)
    full_name: str = Field(max_length=100, nullable=False)
    email: str = Field(max_length=255, unique=True, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship: Allows Python to easily fetch a user's workspaces
    # e.g., current_user.workspaces
    workspaces: list["Workspace"] = Relationship(back_populates="user")


# ==========================================
# 2. THE WORKSPACE ORM MODEL
# ==========================================
class Workspace(SQLModel, table=True):
    __tablename__: str = "workspaces"

    workspace_id: str = Field(primary_key=True, max_length=50)
    user_id: str = Field(foreign_key="users.user_id")
    workspace_name: str = Field(max_length=100, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationships: Links backwards to the owner, and forwards to its records
    user: User = Relationship(back_populates="workspaces")
    records: list["Record"] = Relationship(back_populates="workspace")


# ==========================================
# 3. THE RECORD ORM MODEL
# ==========================================
class Record(SQLModel, table=True):
    __tablename__: str = "records"

    record_id: str = Field(primary_key=True, max_length=50)
    workspace_id: str = Field(foreign_key="workspaces.workspace_id")
    
    # Using the exact key your validation engine outputs
    name: Optional[str] = Field(max_length=100) 
    
    email: str = Field(max_length=255, nullable=False)
    company: Optional[str] = Field(max_length=100)
    city: Optional[str] = Field(max_length=100)
    notes: Optional[str] = Field(default=None)
    
    # Defaulting to False just like your database table safety net
    is_valid: bool = Field(default=False)
    tag: Optional[str] = Field(max_length=50)
    
    # Handled manually by your engine's timestamps
    created_at: Optional[datetime] = Field(default=None)
    processed_at: Optional[datetime] = Field(default=None)

    # Relationship: Allows Python to instantly see which workspace owns this record
    workspace: Workspace = Relationship(back_populates="records")