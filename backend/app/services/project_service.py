from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.project_repo import ProjectRepository
from app.repositories.conversation_repo import ConversationRepository
from app.db.models.project import Project
from app.db.models.prompt import Prompt
from app.db.models.conversation import Conversation
from app.core.exceptions import NotFoundException, ForbiddenException
from app.schemas.project import ProjectCreate, ProjectUpdate
from sqlalchemy import select


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProjectRepository(db)

    async def create(self, user_id: str, data: ProjectCreate) -> Project:
        project = Project(user_id=user_id, **data.model_dump())
        return await self.repo.create(project)

    async def get_all(self, user_id: str) -> list[Project]:
        return await self.repo.get_by_user(user_id)

    async def get_one(self, project_id: str, user_id: str) -> Project:
        project = await self.repo.get_by_id_and_user(project_id, user_id)
        if not project:
            raise NotFoundException("Project")
        return project

    async def update(
        self, project_id: str, user_id: str, data: ProjectUpdate
    ) -> Project:
        project = await self.get_one(project_id, user_id)
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(project, field, value)
        await self.db.flush()
        await self.db.refresh(project)
        return project

    async def delete(self, project_id: str, user_id: str) -> None:
        project = await self.get_one(project_id, user_id)
        project.is_active = False
        await self.db.flush()

    # --- Prompt library ---

    async def add_prompt(
        self, project_id: str, user_id: str, title: str, content: str
    ) -> Prompt:
        await self.get_one(project_id, user_id)
        prompt = Prompt(project_id=project_id, title=title, content=content)
        self.db.add(prompt)
        await self.db.flush()
        await self.db.refresh(prompt)
        return prompt

    async def get_prompts(self, project_id: str, user_id: str) -> list[Prompt]:
        await self.get_one(project_id, user_id)
        result = await self.db.execute(
            select(Prompt).where(Prompt.project_id == project_id)
        )
        return list(result.scalars().all())

    async def delete_prompt(
        self, project_id: str, prompt_id: str, user_id: str
    ) -> None:
        await self.get_one(project_id, user_id)
        result = await self.db.execute(
            select(Prompt).where(
                Prompt.id == prompt_id,
                Prompt.project_id == project_id,
            )
        )
        prompt = result.scalar_one_or_none()
        if not prompt:
            raise NotFoundException("Prompt")
        await self.db.delete(prompt)
        await self.db.flush()