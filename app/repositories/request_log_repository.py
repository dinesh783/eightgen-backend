import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import RequestLog


logger = logging.getLogger("app.repositories.requestlog")


class RequestLogRepository:
    async def create(
        self,
        db: AsyncSession,
        *,
        method: str,
        endpoint: str,
        status_code: int,
        partner_id: int | None = None,
        request_payload: str | None = None,
        response_summary: str | None = None,
    ) -> RequestLog:
        log = RequestLog(
            method=method,
            endpoint=endpoint,
            partner_id=partner_id,
            status_code=status_code,
            request_payload=request_payload,
            response_summary=response_summary,
        )
        try:
            db.add(log)
            await db.commit()
            await db.refresh(log)
            return log
        except SQLAlchemyError:
            await db.rollback()
            logger.exception(
                "Failed to persist request log method=%s endpoint=%s",
                method,
                endpoint,
            )
            raise

    async def list_recent(self, db: AsyncSession, limit: int) -> list[RequestLog]:
        result = await db.execute(
            select(RequestLog).order_by(RequestLog.created_at.desc()).limit(limit)
        )
        return result.scalars().all()
