import json
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_db
from app.services.chat_service import ChatService
from app.schemas.chat import (
    ChatRequest,
    ConversationCreate,
    ConversationResponse,
    MessageResponse,
)
from app.api.deps import get_current_user
from app.db.models.user import User

router = APIRouter(prefix="/projects", tags=["Chat"])


@router.post("/{project_id}/conversations", response_model=ConversationResponse, status_code=201)
async def create_conversation(
    project_id: str,
    data: ConversationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return await service.create_conversation(project_id, current_user.id, data.title)


@router.get("/{project_id}/conversations", response_model=list[ConversationResponse])
async def list_conversations(
    project_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return await service.get_conversations(project_id, current_user.id)


@router.get(
    "/{project_id}/conversations/{conversation_id}/messages",
    response_model=list[MessageResponse],
)
async def get_messages(
    project_id: str,
    conversation_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)
    return await service.get_messages(project_id, conversation_id, current_user.id)


@router.post("/{project_id}/conversations/{conversation_id}/chat")
async def chat(
    project_id: str,
    conversation_id: str,
    data: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ChatService(db)

    async def event_generator():
        try:
            async for chunk in service.stream_response(
                project_id=project_id,
                conversation_id=conversation_id,
                user_id=current_user.id,
                user_message=data.message,
            ):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield f"data: {json.dumps({'done': True})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )