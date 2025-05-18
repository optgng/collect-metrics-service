from fastapi.openapi.utils import get_openapi
from app import create_app

app = create_app()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Monitoring Service API",
        version="1.0.0",
        description=(
            "API для сбора, хранения и экспонирования метрик с серверов и устройств.\n\n"
            "### Основные возможности:\n"
            "- CRUD для устройств мониторинга (`/api/v1/devices`)\n"
            "- Сбор и экспонирование метрик Prometheus (`/api/v1/metrics`)\n"
            "- Проверка состояния сервиса (`/api/v1/health`)\n"
            "\n"
            "Устройства для мониторинга берутся из базы данных, а не из переменных окружения."
        ),
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
