from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship, Session, select

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

    user_id: str = Field(primary_key=True)
    name: str = Field(max_length=100, nullable=False)
    email: str = Field(max_length=255, unique=True, nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship: Allows Python to easily fetch a user's workspaces
    # e.g., current_user.workspaces
    # workspaces: list["Workspace"] = Relationship(back_populates="user")
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

# # ==========================================
# # 2. THE WORKSPACE ORM MODEL
# # ==========================================
# class Workspace(SQLModel, table=True):
#     __tablename__: str = "workspaces"

#     workspace_id: str = Field(primary_key=True, max_length=50)
#     user_id: str = Field(foreign_key="users.user_id")
#     workspace_name: str = Field(max_length=100, nullable=False)
#     created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

#     # Relationships: Links backwards to the owner, and forwards to its records
#     user: User = Relationship(back_populates="workspaces")
#     records: list["Record"] = Relationship(back_populates="workspace")


# # ==========================================
# # 3. THE RECORD ORM MODEL
# # ==========================================
# class Record(SQLModel, table=True):
#     __tablename__: str = "records"

#     record_id: str = Field(primary_key=True, max_length=50)
#     workspace_id: str = Field(foreign_key="workspaces.workspace_id")
    
#     # Using the exact key your validation engine outputs
#     name: Optional[str] = Field(max_length=100) 
    
#     email: str = Field(max_length=255, nullable=False)
#     company: Optional[str] = Field(max_length=100)
#     city: Optional[str] = Field(max_length=100)
#     notes: Optional[str] = Field(default=None)
    
#     # Defaulting to False just like your database table safety net
#     is_valid: bool = Field(default=False)
#     tag: Optional[str] = Field(max_length=50)
    
#     # Handled manually by your engine's timestamps
#     created_at: Optional[datetime] = Field(default=None)
#     processed_at: Optional[datetime] = Field(default=None)

#     # Relationship: Allows Python to instantly see which workspace owns this record
#     workspace: Workspace = Relationship(back_populates="records")

# # make a jobs orm