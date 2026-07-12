from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from app.repositories.user_repository import UserRepository
from app.utils.jwt import verify_access_token
from app.utils.logger import logger

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login'
)

async def get_current_user(token:str = Depends(oauth2_scheme)):
    
    email = verify_access_token(token)
    
    user_repository = UserRepository()
    
    logger.info(f"Finding user attempt for {email}")
    
    db_user = await user_repository.find_user_by_email(email)
    
    if not db_user:
        logger.warning(f"Failed: {email} already exists")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
        
    return db_user

async def get_current_admin(
    current_user: dict = Depends(get_current_user)
):

    if current_user.get("role") != "admin":

        logger.warning(
            f"Unauthorized admin access by {current_user['email']}"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required."
        )

    return current_user