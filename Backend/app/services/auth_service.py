from fastapi import HTTPException, status

from app.schemas.auth import UserLogin
from app.utils.password import verify_password
from app.utils.jwt import create_access_token

from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserRegister
from app.utils.password import hash_password

from app.schemas.auth import UpdateUser, ChangePassword
from app.utils.logger import logger

class AuthService:

    def __init__(self):
        self.user_repository = UserRepository()

    async def register_user(self, user: UserRegister):

        existing_user = await self.user_repository.find_user_by_email(
            user.email
        )

        if existing_user:
            logger.warning(f"Registration failed: {user.email} already exists")
            raise ValueError("Email is already registered.")

        hashed_password = hash_password(user.password)

        user_data = user.model_dump()

        user_data["password"] = hashed_password
        user_data['role'] = 'user'

        user_id = await self.user_repository.create_user(user_data)
        
        logger.info('Regestration successful')
        
        return {
            "message": "User registered successfully.",
            "user_id": str(user_id)
        }
        
    
    async def login_user(self, user: UserLogin):

        db_user = await self.user_repository.find_user_by_email(user.email)

        if not db_user:
            logger.warning(f"Login failed: {user.email} already exists")
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(
            user.password,
            db_user["password"]
        ):
            logger.warning(f"Password Mismatched failed: {user.email}")
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
            
        access_token = create_access_token(
            data={
                "sub": db_user["email"],
                'role':db_user.get('role','user')
            }
        )
        
        logger.info('access token generated succesfully')
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "role": db_user.get("role", "user"),
            "username": db_user["username"]
        }

class UserService:

    def __init__(self):
        self.user_repository = UserRepository()

    async def update_user(
        self,
        user_id: str,
        user: UpdateUser
    ):

        updated_data = user.model_dump()

        await self.user_repository.update_user(
            user_id,
            updated_data
        )
        
        logger.info('User profile updated successfully')
        return {
            "message": "Profile updated successfully."
        }

    async def delete_user(self, user_id: str):

        await self.user_repository.delete_user(user_id)
        logger.info('User profile deleted successfully')
        return {
            "message": "User deleted successfully."
        }

    async def change_password(
        self,
        current_user: dict,
        password_data: ChangePassword
    ):

        if not verify_password(
            password_data.current_password,
            current_user["password"]
        ):
            logger.info('Incorrect password')

            raise HTTPException(
                status_code=400,
                detail="Current password is incorrect."
            )

        new_password = hash_password(
            password_data.new_password
        )

        await self.user_repository.update_user(
            str(current_user["_id"]),
            {
                "password": new_password
            }
        )
        logger.info('Password updated successfully')

        return {
            "message": "Password changed successfully."
        }