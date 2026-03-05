import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Partner
from app.schemas import PartnerCreate


logger = logging.getLogger("app.repositories.partner")


class PartnerRepository:
    async def create(
        self,
        db: AsyncSession,
        partner_in: PartnerCreate,
        api_key_hash: str,
    ) -> Partner:
        partner = Partner(
            name=partner_in.name,
            rate_limit_per_minute=partner_in.rate_limit_per_minute,
            api_key_hash=api_key_hash,
        )
        try:
            db.add(partner)
            await db.commit()
            await db.refresh(partner)
            return partner
        except SQLAlchemyError:
            await db.rollback()
            logger.exception("Failed to create partner name=%s", partner_in.name)
            raise

    async def list_all(self, db: AsyncSession) -> list[Partner]:
        result = await db.execute(select(Partner))
        return result.scalars().all()

    async def get_by_api_key_hash(
        self,
        db: AsyncSession,
        api_key_hash: str,
    ) -> Partner | None:
        result = await db.execute(
            select(Partner).where(Partner.api_key_hash == api_key_hash)
        )
        return result.scalars().first()

    async def update_api_key_hash(
        self,
        db: AsyncSession,
        partner: Partner,
        new_api_key_hash: str,
    ) -> Partner:
        partner.api_key_hash = new_api_key_hash
        try:
            await db.commit()
            await db.refresh(partner)
            return partner
        except SQLAlchemyError:
            await db.rollback()
            logger.exception("Failed to rotate api_key hash for partner id=%s", partner.id)
            raise
