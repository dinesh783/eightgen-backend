from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas import PartnerCreate, PartnerCreateResponse, PartnerOut
from app.services import PartnerService


router = APIRouter(tags=["partners"])
partner_service = PartnerService()


@router.post("/partners", response_model=PartnerCreateResponse)
async def create_partner(
    partner_in: PartnerCreate,
    db: AsyncSession = Depends(get_db),
):
    return await partner_service.create_partner(db, partner_in)


@router.get("/partners", response_model=list[PartnerOut])
async def list_partners(db: AsyncSession = Depends(get_db)):
    return await partner_service.list_partners(db)
