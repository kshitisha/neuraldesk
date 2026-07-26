from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.core.exceptions import UnauthorizedException
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    return pwd_context.hash(password)
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "exp": expire,
        "type": "access",
        "iat": datetime.now(timezone.utc),}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": user_id,
        "exp": expire,
        "type": "refresh",}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
def decode_token(token: str, expected_type: str = "access") -> dict:
    """decodes and validates a JWT token.
    raises UnauthorizedException for any invalid token — expired,
    wrong signature, wrong type. Never leaks why it failed to the client.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        if payload.get("type") != expected_type:
            raise UnauthorizedException("Invalid token type.")

        user_id: Optional[str] = payload.get("sub")
        if user_id is None:
            raise UnauthorizedException("Invalid token payload.")

        return payload
    except JWTError:
        raise UnauthorizedException("token is invalid or expired")