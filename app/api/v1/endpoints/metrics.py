from fastapi import APIRouter
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response

router = APIRouter()

@router.get("/metrics")
async def prometheus_metrics():
    """
    Endpoint для экспонирования метрик в формате Prometheus.
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)