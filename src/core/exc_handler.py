# ruff: noqa: F405
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


async def sectest_exception_handler(request: Request, exc: SecTestException):
    return JSONResponse(
        status_code=resolve_status_code(exc),
        content={"detail": exc.detail},
    )
