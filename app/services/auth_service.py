import logging

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_api_key
from app.models import Partner
from app.repositories import PartnerRepository


logger = logging.getLogger("app.services.auth")


class AuthService:
    def __init__(self, partner_repository: PartnerRepository | None = None):
        self.partner_repository = partner_repository or PartnerRepository()

    async def get_partner_by_api_key(
        self,
        db: AsyncSession,
        api_key: str | None,
    ) -> Partner:
        if api_key is None:
            logger.warning("Authentication failed: missing X-API-Key header")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing X-API-Key header",
            )

        partner = await self.partner_repository.get_by_api_key_hash(
            db,
            hash_api_key(api_key),
        )
        if partner is not None:
            return partner

        # Backward compatibility: support legacy plaintext keys stored in DB,
        # then migrate them to hashed representation on first successful auth.
        legacy_partner = await self.partner_repository.get_by_api_key_hash(db, api_key)
        if legacy_partner is not None:
            logger.warning(
                "Migrating legacy plaintext API key to hash for partner_id=%s",
                legacy_partner.id,
            )
            return await self.partner_repository.update_api_key_hash(
                db,
                legacy_partner,
                hash_api_key(api_key),
            )
        logger.warning("Authentication failed: invalid API key")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
