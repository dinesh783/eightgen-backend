import logging

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import setup_logging
from app.db.base import Base
from app.db.session import engine
# Import models so SQLAlchemy metadata is registered.
from app.models import Partner, RequestLog  # noqa: F401


setup_logging()
logger = logging.getLogger("app")


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name)

    @app.on_event("startup")
    async def startup() -> None:
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database metadata initialized")
        except Exception:
            # Tables can be created later once DB is available.
            logger.exception("Failed to initialize database metadata on startup")

    register_exception_handlers(app)
    app.include_router(api_router)
    return app
