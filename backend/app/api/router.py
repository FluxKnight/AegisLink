from fastapi import APIRouter

from app.api.routes import analyses, health, reports

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(analyses.router)
api_router.include_router(reports.router)
