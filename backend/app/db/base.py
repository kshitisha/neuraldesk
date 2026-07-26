import uuid
from datetime import datetime, timezone
from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,)
from app.core.config import settings
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # logs SQL in development only
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,)
class Base(DeclarativeBase):
    """all models inherit from this.
    gives every table id, created_at, updated_at for free."""
    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=lambda: str(uuid.uuid4()),)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
async def get_db():
    """fastAPI dependency — yields a database session per request
    and guarantees it is closed when the request finishes,
    even if an exception is raised.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()