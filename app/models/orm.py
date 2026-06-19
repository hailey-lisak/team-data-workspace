# What is ORM (object-relational mapping)?
# It acts as a universal translator between Python (object world) and PostgreSQL (relational world)
# Without it, we'd have to write raw SQL text directly inside the Python code if we wanted to save a new user to the database, for example.

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.storage.database import Base

class UserModel(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True,nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WorkspaceModel(Base):
    __tablename__ = "workspaces"

    workspace_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())