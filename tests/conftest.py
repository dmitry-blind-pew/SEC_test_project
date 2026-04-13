# ruff: noqa: E402
import pytest
from httpx import ASGITransport, AsyncClient
from typing import AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from src.api.deps import get_db
from src.core.config import settings
from src.core.db import async_session_maker_null_pool
from src.utils.db_manager import DBManager
from src.main import app


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    """Проверяет, активность TEST мода."""
    assert settings.MODE == "TEST"
    yield


async def get_db_manager_null_pool():
    """Возвращает DBManager на базе NullPool, ограничивая пул соединений до одного"""
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db_manager() -> AsyncGenerator[DBManager, None]:
    """Выдает DBManager для одного теста."""
    async for db in get_db_manager_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_manager_null_pool


def _asgi_transport() -> ASGITransport:
    """
    Создает ASGITransport для внутрипроцессных тестов API.(HTTP-запросы идут напрямую в ASGI-приложение без поднятия
    внешнего сервера)
    """
    return ASGITransport(app=app)


@pytest.fixture
async def api_client() -> AsyncGenerator[AsyncClient, None]:
    """Возвращает API-клиент с корректным X-API-Key."""
    async with AsyncClient(
        transport=_asgi_transport(),
        base_url="http://test",
        headers={"X-API-Key": settings.API_KEY},
    ) as c:
        yield c


@pytest.fixture
async def api_client_wrong_key() -> AsyncGenerator[AsyncClient, None]:
    """Возвращает API-клиент с некорректным X-API-Key."""
    async with AsyncClient(
        transport=_asgi_transport(),
        base_url="http://test",
        headers={"X-API-Key": "wrong"},
    ) as c:
        yield c


@pytest.fixture
async def api_client_no_key() -> AsyncGenerator[AsyncClient, None]:
    """Возвращает API-клиент без заголовка X-API-Key."""
    async with AsyncClient(
        transport=_asgi_transport(),
        base_url="http://test",
    ) as c:
        yield c


@pytest.fixture
async def client_fixture(request) -> AsyncGenerator[AsyncClient, None]:
    """В тесте передает строковое имя нужной фикстуры."""
    client = request.getfixturevalue(request.param)
    yield client
