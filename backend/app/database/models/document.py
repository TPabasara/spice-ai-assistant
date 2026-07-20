from datetime import datetime
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "recipe", "policy", "faq"
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    chunk_count: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # "pending", "processed", "failed"
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)