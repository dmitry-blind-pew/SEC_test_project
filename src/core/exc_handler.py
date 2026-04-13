# ruff: noqa: F405
import logging
from fastapi import Request
from fastapi.responses import JSONResponse

from src.core.domain_exc import *  # noqa F403


EXCEPTION_STATUS_MAP: dict[type[SecTestException], int] = {
    ApiKeyInvalidException: 403,
    ObjectNotFoundException: 404,
    CompanyNotFoundException: 404,
    InvalidRectangleBoundsException: 422,
}


def resolve_status_code(exc: SecTestException) -> int:
    for exc_type, status_code in EXCEPTION_STATUS_MAP.items():
        if isinstance(exc, exc_type):
            return status_code
    return 500

logger = logging.getLogger(__name__)

async def sectest_exception_handler(request: Request, exc: SecTestException):
    status_code = resolve_status_code(exc)
    log_fn = logger.warning if status_code < 500 else logger.error
    log_fn(
        "Обработана ошибка: type=%s status=%s detail=%s method=%s path=%s",
        type(exc).__name__,
        status_code,
        exc.detail,
        request.method,
        request.url.path,
    )
    return JSONResponse(
        status_code=resolve_status_code(exc),
        content={"detail": exc.detail},
    )
