from fastapi import APIRouter

from app.schemas.auth import UserRegister , UserLogin , Token , RegisterResponse
from app.services.auth_service import AuthService
from app.dependencies.auth import get_current_user

router = APIRouter()
auth_service = AuthService()

@router.post("/register")
async def register(user: UserRegister , response_model=RegisterResponse):

    response = await auth_service.register_user(user)
    return response

@router.post("/login",response_model=Token)
async def login(user: UserLogin):
    
    return await auth_service.login_user(user)


