from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
class ProjectFile(Base):
    __tablename__ = "project_files"

    project_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    openai_file_id: Mapped[str] = mapped_column(String(255), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    purpose: Mapped[str] = mapped_column(String(100), default="assistants")
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ready")

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="files")