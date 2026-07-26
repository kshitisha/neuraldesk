from typing import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.project_repo import ProjectRepository
from app.repositories.conversation_repo import ConversationRepository, MessageRepository
from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.llm.factory import get_llm_provider
from app.llm.base import ChatMessage, LLMConfig
from app.core.exceptions import NotFoundException
import logging

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.project_repo = ProjectRepository(db)
        self.conv_repo = ConversationRepository(db)
        self.msg_repo = MessageRepository(db)

    async def create_conversation(
        self, project_id: str, user_id: str, title: str | None = None
    ) -> Conversation:
        project = await self.project_repo.get_by_id_and_user(project_id, user_id)
        if not project:
            raise NotFoundException("Project")

        conversation = Conversation(
            project_id=project_id,
            user_id=user_id,
            title=title or "New Conversation",
        )
        return await self.conv_repo.create(conversation)

    async def get_conversations(
        self, project_id: str, user_id: str
    ) -> list[Conversation]:
        project = await self.project_repo.get_by_id_and_user(project_id, user_id)
        if not project:
            raise NotFoundException("Project")
        return await self.conv_repo.get_by_project(project_id)

    async def get_messages(
        self, project_id: str, conversation_id: str, user_id: str
    ) -> list[Message]:
        project = await self.project_repo.get_by_id_and_user(project_id, user_id)
        if not project:
            raise NotFoundException("Project")

        conversation = await self.conv_repo.get_by_id_and_project(
            conversation_id, project_id
        )
        if not conversation:
            raise NotFoundException("Conversation")

        return await self.msg_repo.get_by_conversation(conversation_id)

    async def stream_response(
        self,
        project_id: str,
        conversation_id: str,
        user_id: str,
        user_message: str,
    ) -> AsyncIterator[str]:
        # Verify ownership
        project = await self.project_repo.get_by_id_and_user(project_id, user_id)
        if not project:
            raise NotFoundException("Project")

        conversation = await self.conv_repo.get_by_id_and_project(
            conversation_id, project_id
        )
        if not conversation:
            raise NotFoundException("Conversation")

       
        user_msg = Message(
            conversation_id=conversation_id,
            role="user",
            content=user_message,
        )
        self.db.add(user_msg)
        await self.db.flush()

       
        history = await self.msg_repo.get_by_conversation(
            conversation_id, limit=20
        )

        
        llm_messages = [
            ChatMessage(role=msg.role, content=msg.content)
            for msg in history
        ]

       
        provider = get_llm_provider(project.provider)
        config = LLMConfig(
            model=project.model,
            temperature=project.temperature,
            system_prompt=project.system_prompt or "",
            provider=project.provider,
        )

        full_response = ""
        async for chunk in provider.stream_chat(llm_messages, config):
            full_response += chunk
            yield chunk

        
        assistant_msg = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=full_response,
        )
        self.db.add(assistant_msg)
        await self.db.flush()