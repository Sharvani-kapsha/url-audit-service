import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger("url-audit")


class RequestIDMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        request_id = str(uuid.uuid4())

        request.state.request_id = request_id

        logger.info(
            f"Request ID={request_id} "
            f"Method={request.method} "
            f"Path={request.url.path}"
        )

        response = await call_next(request)

        response.headers["X-Request-ID"] = request_id

        return response