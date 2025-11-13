from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
try:
    # pgvector provides a SQLAlchemy column type
    from pgvector.sqlalchemy import Vector as VectorType
except Exception:  # pragma: no cover - import fallback for environments without pgvector
    VectorType = None


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(512))
    url: Mapped[str] = mapped_column(String(1024))
    retailer: Mapped[str] = mapped_column(String(64))
    price: Mapped[float] = mapped_column(Float)
    rating: Mapped[float] = mapped_column(Float, default=0)
    features: Mapped[str] = mapped_column(String(2048), default="")  # JSON string for v0
    # optional vector column for semantic search (pgvector)
    if VectorType is not None:
        vector = mapped_column(VectorType(1536), nullable=True)
    else:  # pragma: no cover - fall back to None so imports/tests still run without pgvector
        vector = mapped_column(String(1024), nullable=True)
