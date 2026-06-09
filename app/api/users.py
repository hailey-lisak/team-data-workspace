from fastapi import APIRouter, status
'''
pydantic: acts as a strict data validation gatekeeper
        - BaseModel: builds any data template
                - when we create a class that inherits from it, it grants that class validation powers
                - allows FastAPI to automatically read the class and convert incoming JSON text into a Python object
                - gives access to built-in helper methods which instantly turns validated data back into a standard Python dictionary
''' 
from pydantic import BaseModel, EmailStr
from app.services import user_service

router = APIRouter()

class UserCreateRequest(BaseModel):
    email: EmailStr
    name: str
    

@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreateRequest):
    saved_user = user_service.create_user(
        email = payload.email,
        name = payload.name,
    )
    return saved_user