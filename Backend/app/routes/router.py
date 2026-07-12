from fastapi import APIRouter

from app.routes import auth
from app.routes import users
from app.routes import news

router = APIRouter()

router.include_router(
    auth.router,
    prefix='/auth',
    tags=['Authentication']
)

router.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

router.include_router(
    news.router,
    prefix='/news',
    tags=['News']
)