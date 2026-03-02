from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from .database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(Text)
    ai_response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Partner(Base):
    """
    SQLAlchemy model for API partners.
    """

    __tablename__ = "partners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    api_key = Column(String(64), unique=True, index=True, nullable=False)
    rate_limit_per_minute = Column(Integer, nullable=False, default=60)