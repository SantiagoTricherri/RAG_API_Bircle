import uuid
import time
import logging
from fastapi import Request

logger = logging.getLogger("app")

logging.basicConfig(
    level=logging.INFO,
    format='{"level":"%(levelname)s","message":"%(message)s"}'
)


async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    response = await call_next(request)

    duration = round(time.time() - start_time, 4)

    logger.info(
        f'"request_id":"{request_id}",'
        f'"method":"{request.method}",'
        f'"path":"{request.url.path}",'
        f'"status_code":{response.status_code},'
        f'"duration":{duration}'
    )

    response.headers["X-Request-ID"] = request_id

    return response