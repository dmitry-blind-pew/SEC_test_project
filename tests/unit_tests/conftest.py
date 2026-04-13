from unittest.mock import AsyncMock
from typing import Any

import pytest
from src.api.deps import PaginationParams


@pytest.fixture
def pagination_input() -> PaginationParams:
    """Возвращает объект пагинации для unit-тестов сервисов."""
    return PaginationParams(page=2, per_page=10)


@pytest.fixture
def db_with_companies_repo() -> Any:
    """Создает мок DBManager с моками методов репозитория компаний."""
    class CompaniesRepoMock:
        def __init__(self):
            self.get_in_rectangle = AsyncMock()
            self.get_by_id = AsyncMock()
            self.get_one = AsyncMock()
            self.get_in_radius = AsyncMock()
            self.get_by_name = AsyncMock()
            self.get_filtered = AsyncMock()
            self.get_by_activity = AsyncMock()
            self.get_in_activity = AsyncMock()

    class DBManagerMock:
        def __init__(self):
            self.companies = CompaniesRepoMock()

    return DBManagerMock()
