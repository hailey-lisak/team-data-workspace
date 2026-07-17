'''
uuid = Universally Unique Identifier
    - a way to generate an ID that is guaranteed to be completely unique across the entire universe 
    - protects privacy and safety (compared to just doing user1, user2, etc.)
'''

import uuid
from datetime import datetime, timezone
from database.models import create_user_db
from sqlmodel import Session
from sqlmodel import select
from database.models import User

def create_user(db: Session, email: str, name: str) -> dict:
    '''
    Generates a random ID, strips hyphens (.hex), and cuts it down to the first 8 characters ([:8])
    '''
    user_id = f"usr_{uuid.uuid4().hex[:8]}"
    created_at = datetime.now(timezone.utc).isoformat()
    
    '''
    new_user = dictionary
        - white space is stripped
        - email is all lowercase 
    '''
    new_user = {
        "user_id": user_id,
        "name": name.strip(),
        "email": email.strip().lower(),
        "created_at": created_at
    }

    #save to database where the orm comes in to play instead of printing
    #this is how the functions in the orm connects to the api
    #once its saved it has to be persistent 100% before it can be used for anything ekse
    #all we do is call the function and let the library handle it 

    #work on orm and trace the call, create diagram on how its functioning
    """ print("\n"+"="*40)
    print("STORAGE EVENT: TEMPORARY PRINT OUT")
    print(f"Successfully Created New User Profile:")
    print(f" - User ID: {new_user['user_id']}")
    print(f" - Name: {new_user['name']}")
    print(f" - Email: {new_user['email']}")
    print(f" - Created At: {new_user['created_at']}")
    print("="*40 + "\n") """
    create_user_db(session=db, user_data=new_user)
    return new_user

def get_all_users(db: Session) -> list:
    """
    Retrieves all users from the database.
    """
    # Fetch the raw database objects
    users = db.exec(select(User)).all()
    
    # Map them to simple dictionaries so our API layer gets clean data
    formatted_users = []
    for user in users:
        if hasattr(user, "model_dump"):
            formatted_users.append(user.model_dump())
        elif hasattr(user, "dict"):
            formatted_users.append(user.dict())
        else:
            # If it comes back as a join tuple, handle the nested 'User' object
            user_obj = getattr(user, "User", user)
            if hasattr(user_obj, "model_dump"):
                formatted_users.append(user_obj.model_dump())
            else:
                formatted_users.append(dict(user_obj))
                
    return formatted_users

def delete_user(db: Session, user_id: str) -> bool:
    """
    Business logic for removing a user. 
    Verifies existence before triggering db deletion.
    """
    user = db.get(User, user_id)
    if not user:
        return False
        
    db.delete(user)
    db.commit()
    return True

def update_user(db: Session, user_id: str, email: str | None = None, name: str | None = None) -> dict | None:
    """
    Business logic for updating user details.
    Ensures input is normalized (stripped and lowercased) before saving.
    """
    user = db.get(User, user_id)
    if not user:
        return None
        
    # Apply our normalization rules if updates are provided
    if name is not None:
        user.name = name.strip()
    if email is not None:
        user.email = email.strip().lower()
        
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Return as a dictionary matching our schema output
    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "created_at": user.created_at
    }