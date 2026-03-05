import logging
import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_api_key
from app.repositories import PartnerRepository
from app.schemas import PartnerCreate, PartnerCreateResponse


logger = logging.getLogger("app.services.partner")


class PartnerService:
    def __init__(self, partner_repository: PartnerRepository | None = None):
        self.partner_repository = partner_repository or PartnerRepository()

    async def create_partner(
        self,
        db: AsyncSession,
        partner_in: PartnerCreate,
    ) -> PartnerCreateResponse:
        api_key = secrets.token_hex(16)
        api_key_hash = hash_api_key(api_key)
        partner = await self.partner_repository.create(db, partner_in, api_key_hash)
        logger.info("Created partner id=%s name=%s", partner.id, partner.name)
        return PartnerCreateResponse(
            id=partner.id,
            name=partner.name,
            rate_limit_per_minute=partner.rate_limit_per_minute,
            api_key=api_key,
        )

    async def list_partners(self, db: AsyncSession):
        partners = await self.partner_repository.list_all(db)
        logger.info("Fetched partners count=%s", len(partners))
        return partners
