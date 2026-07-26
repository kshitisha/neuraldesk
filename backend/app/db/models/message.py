from sqlalchemy import String, Text, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
class Message(Base):
    __tablename__ = "messages"

    conversation_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)  # user | assistant
    content: Mapped[str] = mapped_column(Text, nullable=False)
    token_count: Mapped[int] = mapped_column(Integer, nullable=True)

    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")