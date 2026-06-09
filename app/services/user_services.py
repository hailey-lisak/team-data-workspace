'''
uuid = Universally Unique Identifier
    - a way to generate an ID that is guaranteed to be completely unique across the entire universe 
    - protects privacy and safety (compared to just doing user1, user2, etc.)
'''

import uuid
def create_user(name: str, email: str) -> dict:
    '''
    Generates a random ID, strips hyphens (.hex), and cuts it down to the first 8 characters ([:8])
    '''
    user_id = f"usr_{uuid.uuid4().hex[:8]}"
    
    '''
    new_user = dictionary
        - white space is stripped
        - email is all lowercase 
    '''
    new_user = {
        "user_id": user_id,
        "name": name.strip(),
        "email": email.strip().lower()
    }

    print("\n"+"="*40)
    print("STORAGE EVENT: TEMPORARY PRINT OUT")
    print(f"Successfully Creted New User Profile:")
    print(f" - User ID: {new_user['user_id']}")
    print(f" - Name: {new_user['name']}")
    print(f" - Email: {new_user['email']}")
    print("="*40 + "\n")

    return new_user
