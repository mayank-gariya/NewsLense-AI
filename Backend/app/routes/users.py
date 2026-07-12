from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.schemas.auth import UserResponse
from app.schemas.auth import UpdateUser, ChangePassword
from app.services.auth_service import UserService

router = APIRouter()

user_service = UserService()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user["_id"]),
        "username": current_user["username"],
        "email": current_user["email"],
        "role": current_user.get("role", "user")
    }


@router.put("/update")
async def update_profile(
    user: UpdateUser,
    current_user=Depends(get_current_user)
):

    return await user_service.update_user(
        str(current_user["_id"]),
        user
    )


@router.delete("/delete")
async def delete_profile(
    current_user=Depends(get_current_user)
):

    return await user_service.delete_user(
        str(current_user["_id"])
    )


@router.patch("/change-password")
async def change_password(
    password_data: ChangePassword,
    current_user=Depends(get_current_user)
):

    return await user_service.change_password(
        current_user,
        password_data
    )
