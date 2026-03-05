from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text

from app.db.base import Base


class RequestLog(Base):
    __tablename__ = "request_logs"

    id = Column(Integer, primary_key=True, index=True)
    method = Column(String(10), nullable=False)
    endpoint = Column(String(255), nullable=False)
    partner_id = Column(Integer, ForeignKey("partners.id"), nullable=True)
    status_code = Column(Integer, nullable=False)
    request_payload = Column(Text, nullable=True)
    response_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
