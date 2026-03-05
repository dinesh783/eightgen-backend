from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas import RequestLogOut
from app.services import RequestLogService


router = APIRouter(tags=["requests"])
request_log_service = RequestLogService()


@router.get("/requests", response_model=list[RequestLogOut])
async def list_requests(limit: int = 50, db: AsyncSession = Depends(get_db)):
    return await request_log_service.list_recent(db, limit)
