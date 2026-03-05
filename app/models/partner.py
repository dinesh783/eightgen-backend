from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Partner(Base):
    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    # Mapped to existing "api_key" DB column; stores hashed value only.
    api_key_hash = Column("api_key", String(64), unique=True, index=True, nullable=False)
    rate_limit_per_minute = Column(Integer, nullable=False, default=60)
