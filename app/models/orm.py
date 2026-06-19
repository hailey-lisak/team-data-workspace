# What is ORM (object-relational mapping)?
# It acts as a universal translator between Python (object world) and PostgreSQL (relational world)
# Without it, we'd have to write raw SQL text directly inside the Python code if we wanted to save a new user to the database, for example.

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.storage.database import Base

class UserModel(Base):

    # Physical name of the table inside the db container
    __tablename__ = "users"

    # Column(): tells db to create a vertical column
    # String: specifies that the column will store text
    # primary_key=True: means that this field is the absolute unique identity card for this row
    #                   - no two users can ever have the same user_id; also ensures field cannot be blank
    # index=True: tells PostgreSQL to create a hidden, optimized search index for this column
    #             - like the index of a textbook; prevents scanning millions of rows one by one
    user_id = Column(String, primary_key=True, index=True)

    # nullable=False: "this field is strictly required"
    #                  - PostgreSQL will instantly block and throw an error if the FastAPI application tries to save a user without a name
    name = Column(String, nullable=False)

    # unique=True: enforces that no two rows can share the same text in this column
    #              - example: no two accounts can use the same email 
    email = Column(String, unique=True,nullable=False, index=True)

    # DataTime(timesoze=True): tells the column to store a full date and time stamp, and explicityl track the time zone
    # server_default=func.now(): "if the Python code forgets to provide a timestamp when creating a user,
    #                             don't crash. Instead, look at the server's internal clock right now and stamp the current time automatically."
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class WorkspaceModel(Base):
    __tablename__ = "workspaces"

    workspace_id = Column(String, primary_key=True, index=True)

    #ForeignKey("users.user_id"): establishes a relationship between my tables 
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Why would index ever be False?
# Because it comes with a cost.
# Everytime we set eindex=True, PostgreSQL builds a hidden companion table to speed up searches
# The Penalty: everytime we insert a new user or update a name, PostgreSQL has to stop and rewrite those index files.
#       If we index every column, saving data becomes incredibly slow.
# The Rule of Thumb: only set index=True on columns you know you will use constantly in yur code's search queries 
#       (like IDs, emails, usernames). For everything else (like a profile bio), leave it False.
