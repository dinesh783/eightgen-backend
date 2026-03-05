from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.partners import router as partners_router
from app.api.routes.proxy import router as proxy_router
from app.api.routes.requests import router as requests_router


api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(partners_router)
api_router.include_router(requests_router)
api_router.include_router(proxy_router)
