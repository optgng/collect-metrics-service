from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routers import api_router
from app.core.logging import setup_logging
from app.middleware import LoggingMiddleware
from app.core.config import settings

def create_app():
    setup_logging()
    app = FastAPI(title="CloudNativeService", openapi_url="/openapi.json")
    app.include_router(api_router, prefix="/api/v1")
    app.add_middleware(LoggingMiddleware)
    # Параметризация CORS через настройки
    allow_origins = getattr(settings, "CORS_ALLOW_ORIGINS", ["http://webui.localhost:3000"])
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
