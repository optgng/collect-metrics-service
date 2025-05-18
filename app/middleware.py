from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time

logger = logging.getLogger("app.middleware")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = time.time() - start
        logger.info(
            "path=%s method=%s status_code=%d duration=%.3f", request.url.path, request.method, response.status_code, duration
        )
        return response
