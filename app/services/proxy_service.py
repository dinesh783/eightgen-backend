import logging

import httpx
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models import Partner
from app.services.rate_limit_service import RateLimitService
from app.services.request_log_service import RequestLogService


logger = logging.getLogger("app.services.proxy")


class ProxyService:
    def __init__(
        self,
        rate_limit_service: RateLimitService | None = None,
        request_log_service: RequestLogService | None = None,
    ):
        self.rate_limit_service = rate_limit_service or RateLimitService()
        self.request_log_service = request_log_service or RequestLogService()

    async def proxy_get(
        self,
        db: AsyncSession,
        *,
        partner: Partner,
        proxy_path: str,
        upstream_path: str,
    ):
        self.rate_limit_service.enforce(partner)

        upstream_url = f"{settings.jsonplaceholder_base_url}/{upstream_path}"
        logger.info(
            "Proxy request partner_id=%s path=%s upstream=%s",
            partner.id,
            proxy_path,
            upstream_url,
        )

        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(upstream_url, timeout=10)
        except httpx.RequestError as exc:
            logger.exception("Upstream request failed url=%s", upstream_url)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Upstream service unavailable",
            ) from exc

        await self.request_log_service.create(
            db,
            method="GET",
            endpoint=proxy_path,
            partner_id=partner.id,
            status_code=resp.status_code,
            response_summary=resp.text[:500],
        )

        if resp.status_code >= 400:
            logger.warning(
                "Upstream returned error status=%s path=%s",
                resp.status_code,
                proxy_path,
            )
            raise HTTPException(
                status_code=resp.status_code,
                detail=f"Upstream error: {resp.text}",
            )

        return resp.json()
