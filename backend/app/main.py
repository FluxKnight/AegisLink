from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.db.database import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title=settings.app_name,
        description=(
            "Defensive URL risk analysis API. Static pattern checks only — "
            "no live website interaction."
        ),
        version="1.0.0",
        lifespan=lifespan,
    )
    application.include_router(api_router)
    return application


app = create_app()
