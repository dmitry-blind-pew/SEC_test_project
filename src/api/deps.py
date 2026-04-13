import logging
from collections.abc import AsyncGenerator
from typing import Annotated
from fastapi import Depends, Security, Query, Request
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

from src.core.config import settings
from src.core.db import async_session_maker
from src.core.domain_exc import ApiKeyInvalidException
from src.utils.db_manager import DBManager


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

logger = logging.getLogger(__name__)

def verify_api_key(request: Request, api_key: str | None = Security(api_key_header)) -> None:
    if api_key != settings.API_KEY:
        logger.warning(
            "Отклонен запрос с неверным API-ключом: method=%s path=%s client_ip=%s",
            request.method,
            request.url.path,
            request.client.host if request.client else "unknown",
        )
        raise ApiKeyInvalidException()


ApiKeyDep = Annotated[str, Depends(verify_api_key)]


async def get_db() -> AsyncGenerator[DBManager, None]:
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]


class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, ge=1, description="Страница")]
    per_page: Annotated[int, Query(20, ge=1, le=100, description="Количество элементов на странице")]


PagDep = Annotated[PaginationParams, Depends()]
