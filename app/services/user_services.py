'''
uuid = Universally Unique Identifier
    - a way to generate an ID that is guaranteed to be completely unique across the entire universe 
    - protects privacy and safety (compared to just doing user1, user2, etc.)
'''

import uuid
from datetime import datetime, timezone
from database.models import create_user_db

def create_user(db, email: str, name: str) -> dict:
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
