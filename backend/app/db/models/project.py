from sqlalchemy import String, Text, Float, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
class Project(Base):
    __tablename__ = "projects"

    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    system_prompt: Mapped[str] = mapped_column(Text, nullable=True)
    model: Mapped[str] = mapped_column(String(100), default="gpt-4o")
    temperature: Mapped[float] = mapped_column(Float, default=0.7)
    provider: Mapped[str] = mapped_column(String(50), default="openai")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    owner: Mapped["User"] = relationship("User", back_populates="projects")
    prompts: Mapped[list["Prompt"]] = relationship(
        "Prompt", back_populates="project", cascade="all, delete-orphan"
    )
    conversations: Mapped[list["Conversation"]] = relationship(
        "Conversation", back_populates="project", cascade="all, delete-orphan"
    )
    files: Mapped[list["ProjectFile"]] = relationship(
        "ProjectFile", back_populates="project", cascade="all, delete-orphan"
    )