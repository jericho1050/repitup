from models import User 
from fastapi import Request, HTTPException

def get_db_uri(user, password, host, db):
    return f'postgres://{user}:{password}@{host}:5432/{db}'
    

async def get_authenticated_user(request: Request) -> User:
    """
    Extract and validate the authenticated user from the request.

    Args:
        request (Request): The incoming request object.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the user is unauthorized.
    """
    user_dict = request.state.user.dict()
    if not user_dict:
        raise HTTPException(status_code=401, detail="Unauthorized User")
    user, _ = await User.get_or_create(object_id=user_dict["sub"])
    return user

if __name__ == "__main__":
    pass