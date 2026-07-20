from datetime import datetime
from sqlalchemy import String, Text, Float, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.session import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(50), index=True, nullable=False)  # e.g., "Whole Spices", "Ground", "Blends"
    price: Mapped[float] = mapped_column(Float, nullable=False)
    stock_quantity: Mapped[int] = mapped_column(Integer, default=0)
    is_organic: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    image_url: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)