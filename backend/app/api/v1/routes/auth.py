from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.services.auth_service import AuthService
from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    RefreshRequest,
    UserResponse,
)
from app.api.deps import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    user = await service.register(data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.refresh(data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user