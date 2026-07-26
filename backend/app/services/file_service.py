from sqlalchemy.ext.asyncio import AsyncSession
from openai import AsyncOpenAI
from app.core.config import settings
from app.repositories.project_repo import ProjectRepository
from app.db.models.file import ProjectFile
from app.core.exceptions import NotFoundException, LLMException
from sqlalchemy import select
import logging
logger = logging.getLogger(__name__)
class FileService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def upload_file(
        self,
        project_id: str,
        user_id: str,
        filename: str,
        file_bytes: bytes,
    ) -> ProjectFile:
        project = await self.project_repo.get_by_id_and_user(project_id, user_id)
        if not project:
            raise NotFoundException("Project")

        try:
            response = await self.client.files.create(
                file=(filename, file_bytes),
                purpose="assistants",
            )
        except Exception as e:
            logger.error(f"OpenAI file upload error: {e}")
            raise LLMException(f"File upload failed: {str(e)}")

        project_file = ProjectFile(
            project_id=project_id,
            openai_file_id=response.id,
            filename=filename,
            purpose="assistants",
            size_bytes=len(file_bytes),
            status="ready",
        )
        self.db.add(project_file)
        await self.db.flush()
        await self.db.refresh(project_file)
        return project_file

    async def get_files(self, project_id: str, user_id: str) -> list[ProjectFile]:
        project = await self.project_repo.get_by_id_and_user(project_id, user_id)
        if not project:
            raise NotFoundException("Project")

        result = await self.db.execute(
            select(ProjectFile).where(ProjectFile.project_id == project_id)
        )
        return list(result.scalars().all())

    async def delete_file(
        self, project_id: str, file_id: str, user_id: str
    ) -> None:
        project = await self.project_repo.get_by_id_and_user(project_id, user_id)
        if not project:
            raise NotFoundException("Project")

        result = await self.db.execute(
            select(ProjectFile).where(
                ProjectFile.id == file_id,
                ProjectFile.project_id == project_id,
            )
        )
        file = result.scalar_one_or_none()
        if not file:
            raise NotFoundException("File")

        try:
            await self.client.files.delete(file.openai_file_id)
        except Exception as e:
            logger.warning(f"OpenAI file delete warning: {e}")

        await self.db.delete(file)
        await self.db.flush()