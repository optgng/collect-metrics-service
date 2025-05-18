from fastapi import APIRouter
from app.api.v1.endpoints import health, metrics
from app.api.v1.endpoints import devices

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
api_router.include_router(devices.router, prefix="/devices", tags=["devices"])
