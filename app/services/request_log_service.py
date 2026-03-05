import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import RequestLogRepository


logger = logging.getLogger("app.services.requestlog")


class RequestLogService:
    def __init__(self, request_log_repository: RequestLogRepository | None = None):
        self.request_log_repository = request_log_repository or RequestLogRepository()

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
    ):
        return await self.request_log_repository.create(
            db,
            method=method,
            endpoint=endpoint,
            status_code=status_code,
            partner_id=partner_id,
            request_payload=request_payload,
            response_summary=response_summary,
        )

    async def list_recent(self, db: AsyncSession, limit: int):
        safe_limit = max(1, min(limit, 200))
        logs = await self.request_log_repository.list_recent(db, safe_limit)
        logger.info("Fetched request logs count=%s", len(logs))
        return logs
