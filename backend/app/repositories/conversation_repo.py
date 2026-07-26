from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.repositories.base import BaseRepository
class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, db: AsyncSession):
        super().__init__(Conversation, db)

    async def get_by_project(self, project_id: str) -> list[Conversation]:
        result = await self.db.execute(
            select(Conversation)
            .where(Conversation.project_id == project_id)
            .order_by(Conversation.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id_and_project(
        self, conversation_id: str, project_id: str
    ) -> Conversation | None:
        result = await self.db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.project_id == project_id,
            )
        )
        return result.scalar_one_or_none()


class MessageRepository(BaseRepository[Message]):
    def __init__(self, db: AsyncSession):
        super().__init__(Message, db)

    async def get_by_conversation(
        self, conversation_id: str, limit: int = 50
    ) -> list[Message]:
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())