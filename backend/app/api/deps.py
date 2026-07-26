from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.core.security import decode_token
from app.core.exceptions import UnauthorizedException
from app.db.models.user import User
from app.repositories.user_repo import UserRepository

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    FastAPI dependency — extracts and validates the JWT from the
    Authorization header, then loads the user from the database.
    Inject this into any route that requires authentication.
    """

    # ---- DEBUG START ----
    token = credentials.credentials
    print("=" * 60)
    print("TOKEN:")
    print(token)

    try:
        payload = decode_token(token, expected_type="access")
        print("PAYLOAD:")
        print(payload)
    except Exception as e:
        print("DECODE TOKEN ERROR:", repr(e))
        raise

    user_id = payload.get("sub")
    print("USER_ID:", user_id)

    repo = UserRepository(db)

    try:
        user = await repo.get_by_id(user_id)
        print("USER:", user)
    except Exception as e:
        print("DATABASE ERROR:", repr(e))
        raise

    if not user:
        print("User not found in database.")
        raise UnauthorizedException("User not found or inactive.")

    print("USER ACTIVE:", user.is_active)

    if not user.is_active:
        print("User exists but is inactive.")
        raise UnauthorizedException("User not found or inactive.")

    print("Authentication successful.")
    print("=" * 60)
    # ---- DEBUG END ----

    return user