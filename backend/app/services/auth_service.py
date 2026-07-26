from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import UserRepository
from app.db.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.core.exceptions import ConflictException, UnauthorizedException
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse


class AuthService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, data: RegisterRequest) -> User:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ConflictException("A user with this email already exists.")

        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
        )
        return await self.repo.create(user)

    async def login(self, data: LoginRequest) -> TokenResponse:
        user = await self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, user.hashed_password):
            raise UnauthorizedException("Invalid email or password.")

        if not user.is_active:
            raise UnauthorizedException("Account is disabled.")

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def refresh(self, refresh_token: str) -> TokenResponse:
        payload = decode_token(refresh_token, expected_type="refresh")
        user_id = payload.get("sub")

        user = await self.repo.get_by_id(user_id)
        if not user or not user.is_active:
            raise UnauthorizedException("User not found or inactive.")

        return TokenResponse(
            access_token=create_access_token(user.id),
            refresh_token=create_refresh_token(user.id),
        )

    async def get_user_by_id(self, user_id: str) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise UnauthorizedException("User not found.")
        return user