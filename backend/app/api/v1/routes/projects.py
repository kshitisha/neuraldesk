from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.services.project_service import ProjectService
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.schemas.chat import PromptCreate, PromptResponse
from app.api.deps import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    data: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService(db)
    return await service.create(current_user.id, data)


@router.get("", response_model=list[ProjectResponse])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService(db)
    return await service.get_all(current_user.id)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService(db)
    return await service.get_one(project_id, current_user.id)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    data: ProjectUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService(db)
    return await service.update(project_id, current_user.id, data)


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService(db)
    await service.delete(project_id, current_user.id)


# --- Prompt library ---

@router.post("/{project_id}/prompts", response_model=PromptResponse, status_code=201)
async def add_prompt(
    project_id: str,
    data: PromptCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService(db)
    return await service.add_prompt(project_id, current_user.id, data.title, data.content)


@router.get("/{project_id}/prompts", response_model=list[PromptResponse])
async def list_prompts(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService(db)
    return await service.get_prompts(project_id, current_user.id)


@router.delete("/{project_id}/prompts/{prompt_id}", status_code=204)
async def delete_prompt(
    project_id: str,
    prompt_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ProjectService(db)
    await service.delete_prompt(project_id, prompt_id, current_user.id)