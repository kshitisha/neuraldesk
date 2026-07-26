from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.services.file_service import FileService
from app.schemas.file import FileResponse
from app.api.deps import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/projects", tags=["Files"])


@router.post("/{project_id}/files", response_model=FileResponse, status_code=201)
async def upload_file(
    project_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FileService(db)
    file_bytes = await file.read()
    return await service.upload_file(
        project_id=project_id,
        user_id=current_user.id,
        filename=file.filename,
        file_bytes=file_bytes,
    )


@router.get("/{project_id}/files", response_model=list[FileResponse])
async def list_files(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FileService(db)
    return await service.get_files(project_id, current_user.id)


@router.delete("/{project_id}/files/{file_id}", status_code=204)
async def delete_file(
    project_id: str,
    file_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = FileService(db)
    await service.delete_file(project_id, file_id, current_user.id)