import logging

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models import Partner
from app.services import AuthService


logger = logging.getLogger("app.api.deps")
auth_service = AuthService()


async def get_current_partner(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    db: AsyncSession = Depends(get_db),
) -> Partner:
    partner = await auth_service.get_partner_by_api_key(db, x_api_key)
    logger.info("Authenticated partner_id=%s", partner.id)
    return partner
