from fastapi import APIRouter
from app.api.v1.routes import auth, projects, chat, files

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(chat.router)
api_router.include_router(files.router)