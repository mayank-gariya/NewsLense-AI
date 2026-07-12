from fastapi import FastAPI
from app.routes.router import router
from app.config.database import db

app = FastAPI(
    title="NewsLens AI",
    version="1.5.0"
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "message": "Welcome to NewsLens AI 🚀"
    }