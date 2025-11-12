from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(512))
    url: Mapped[str] = mapped_column(String(1024))
    retailer: Mapped[str] = mapped_column(String(64))
    price: Mapped[float] = mapped_column(Float)
    rating: Mapped[float] = mapped_column(Float, default=0)
    features: Mapped[str] = mapped_column(String(2048), default="")  # JSON string for v0
