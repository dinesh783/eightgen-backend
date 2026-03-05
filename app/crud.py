from sqlalchemy.ext.asyncio import AsyncSession

from app.services import RequestLogService


async def save_request_log(
    db: AsyncSession,
    method: str,
    endpoint: str,
    status_code: int,
    partner_id: int | None = None,
    request_payload: str | None = None,
    response_summary: str | None = None,
):
    service = RequestLogService()
    return await service.create(
        db,
        method=method,
        endpoint=endpoint,
        status_code=status_code,
        partner_id=partner_id,
        request_payload=request_payload,
        response_summary=response_summary,
    )
