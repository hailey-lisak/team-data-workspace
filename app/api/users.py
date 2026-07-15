from fastapi import APIRouter, status
'''
pydantic: acts as a strict data validation gatekeeper
        - BaseModel: builds any data template
                - when we create a class that inherits from it, it grants that class validation powers
                - allows FastAPI to automatically read the class and convert incoming JSON text into a Python object
                - gives access to built-in helper methods which instantly turns validated data back into a standard Python dictionary
''' 
from pydantic import BaseModel, EmailStr
from app.services import user_services

from sqlmodel import Session
from database.connection import engine
from database.models import create_user_db
'''
let's us split endpoints into small, dedicated files
'''
router = APIRouter()

'''
Stores email and name data while verifying that the data is safe and correctly formatted
Belongs to the API layer, job is external -> faces public internet and handles validation

BaseModel: translates incoming raw JSON text into a clean Python object
            - checks every piece of incoming data against the specified types
            - automatically builds my interactive Swagger API documentation page
                    (which reads class and says exacly what fields my API expects to recieve)
'''
class UserCreateRequest(BaseModel):
    email: EmailStr
    name: str
    
'''
@router -> registers the route with FastAPI, so it knows to listen for incoming requests at this endpoint
.post and /users -> specifies that this endpoint will only respond to POST requests at the /users address
status_code -> standardized, three-digit number that a server sends back to tell a client how the request went (201 means "Created")
------
Belongs to the Service Layer, job is internal
Handles the core business logic and does the heavy lifting
------
payload: the actual data being carried in the body of the request
    - the raw bundle of data being sent over the server
'''
""" @router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateRequest): 
    saved_user = user_services.create_user(
        email = payload.email,
        name = payload.name,
    )
    # ─── 2. ADD THIS SESSION BLOCK AT THE END ─────────────────
    with Session(engine) as session:
        db_user = create_user_db(session=session, user_data=saved_user)
    # ─────────────────────────────────────────────────────────
    return saved_user """
@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateRequest): 
    # 1. Open the database session first
    with Session(engine) as session:
        # 2. Pass the session ('db') into your service
        saved_user = user_services.create_user(
            email=payload.email,
            name=payload.name,
            db=session  # <--- This passes the required 'db' argument!
        )
        
    # 3. Return the saved user data
    return saved_user