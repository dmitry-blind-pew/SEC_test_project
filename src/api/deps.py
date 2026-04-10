from typing import Annotated
from fastapi import Depends, Security
from fastapi.security import APIKeyHeader

from src.core.config import settings
from src.core.db import async_session_maker
from src.core.domain_exc import ApiKeyInvalidException
from src.utils.db_manager import DBManager


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str | None = Security(api_key_header)):
    if api_key != settings.API_KEY:
        raise ApiKeyInvalidException()


ApiKeyDep = Annotated[str, Depends(verify_api_key)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]