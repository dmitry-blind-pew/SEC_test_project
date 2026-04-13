from typing import Any, NoReturn

import pytest
from sqlalchemy import Integer, String
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from unittest.mock import AsyncMock

from src.core.domain_exc import ObjectNotFoundException
from src.repositories.base import BaseRepo


class Base(DeclarativeBase):
    pass


class TestModelORM(Base):
    __tablename__ = "test_model"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))


class TestMapper:
    @staticmethod
    def map_to_domain_entity(model: TestModelORM) -> dict[str, Any]:
        """Мапит тестовую модель в простой словарь."""
        return {"id": model.id, "name": model.name}


class TestRepo(BaseRepo):
    model = TestModelORM
    mapper = TestMapper


class ScalarResultOne:
    def __init__(self, value):
        self._value = value

    def one(self) -> TestModelORM:
        """Возвращает сохраненный объект, имитируя scalar result."""
        return self._value


class ScalarResultNoRows:
    def one(self) -> NoReturn:
        """Имитирует отсутствие строк, как one() в SQLA."""
        raise NoResultFound()


class ExecuteResult:
    def __init__(self, scalar_result):
        """Сохраняет объект, который будет возвращен из scalars()."""
        self._scalar_result = scalar_result

    def scalars(self) -> ScalarResultOne | ScalarResultNoRows:
        """Возвращает имитацию ScalarResult."""
        return self._scalar_result


@pytest.mark.asyncio
async def test_get_one_returns_mapped_entity() -> None:
    """Проверяет, что BaseRepo.get_one возвращает замапленный объект."""
    model = TestModelORM(id=1, name="ACME Corp")
    execute_result = ExecuteResult(ScalarResultOne(model))
    session = type("SessionMock", (), {"execute": AsyncMock(return_value=execute_result)})()
    repo = TestRepo(session=session)

    out = await repo.get_one(id=1)

    assert out == {"id": 1, "name": "ACME Corp"}
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_one_raises_object_not_found() -> None:
    """Проверяет, что BaseRepo.get_one кидает ObjectNotFoundException при пустом результате."""
    execute_result = ExecuteResult(ScalarResultNoRows())
    session = type("SessionMock", (), {"execute": AsyncMock(return_value=execute_result)})()
    repo = TestRepo(session=session)

    with pytest.raises(ObjectNotFoundException):
        await repo.get_one(id=999)
