from typing import Generic, TypeVar, Type
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Generic async CRUD base.
    Every repository inherits this and gets basic operations for free.
    Specific queries live in the child repository — not here.
    """

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    async def get_by_id(self, id: str) -> ModelType | None:
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> list[ModelType]:
        result = await self.db.execute(select(self.model))
        return list(result.scalars().all())

    async def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        await self.db.flush()  # flush to get the ID without committing
        await self.db.refresh(obj)
        return obj

    async def delete(self, obj: ModelType) -> None:
        await self.db.delete(obj)
        await self.db.flush()