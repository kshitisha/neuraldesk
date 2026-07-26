from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.project import Project
from app.repositories.base import BaseRepository
class ProjectRepository(BaseRepository[Project]):
    def __init__(self, db: AsyncSession):
        super().__init__(Project, db)

    async def get_by_user(self, user_id: str) -> list[Project]:
        result = await self.db.execute(
            select(Project)
            .where(Project.user_id == user_id, Project.is_active == True)
            .order_by(Project.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id_and_user(self, project_id: str, user_id: str) -> Project | None:
        result = await self.db.execute(
            select(Project).where(
                Project.id == project_id,
                Project.user_id == user_id,
                Project.is_active == True,
            )
        )
        return result.scalar_one_or_none()