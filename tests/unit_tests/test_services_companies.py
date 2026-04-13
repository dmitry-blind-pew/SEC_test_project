from unittest.mock import AsyncMock

import pytest

from src.core.domain_exc import (
    CompanyNotFoundException,
    InvalidRectangleBoundsException,
    ObjectNotFoundException,
)
from src.services.companies import CompaniesService


@pytest.mark.asyncio
async def test_get_in_rectangle_raises_invalid_bounds(db_with_companies_repo, pagination_input):
    """Проверяет, что сервис отклоняет прямоугольник с min > max."""
    service = CompaniesService(db=db_with_companies_repo)

    with pytest.raises(InvalidRectangleBoundsException):
        await service.get_in_rectangle(
            pagination=pagination_input,
            min_lon=30.0,
            min_lat=53.0,
            max_lon=20.0,
            max_lat=54.0,
        )


@pytest.mark.asyncio
async def test_get_in_rectangle_calls_repo_with_limit_offset(db_with_companies_repo, pagination_input):
    """Проверяет корректный прокид limit/offset в repo.get_in_rectangle."""
    expected_payload = ["ok"]
    db_with_companies_repo.companies.get_in_rectangle = AsyncMock(return_value=expected_payload)
    service = CompaniesService(db=db_with_companies_repo)

    result = await service.get_in_rectangle(
        pagination=pagination_input,
        min_lon=27.5,
        min_lat=53.8,
        max_lon=27.9,
        max_lat=54.0,
    )

    assert result == expected_payload
    db_with_companies_repo.companies.get_in_rectangle.assert_awaited_once_with(
        min_lon=27.5,
        min_lat=53.8,
        max_lon=27.9,
        max_lat=54.0,
        limit=10,
        offset=10,
    )


@pytest.mark.asyncio
async def test_get_by_id_maps_not_found_exception(db_with_companies_repo):
    """Проверяет маппинг ObjectNotFoundException в CompanyNotFoundException."""
    db_with_companies_repo.companies.get_one = AsyncMock(side_effect=ObjectNotFoundException())
    service = CompaniesService(db=db_with_companies_repo)

    with pytest.raises(CompanyNotFoundException):
        await service.get_by_id(company_id=999)


@pytest.mark.asyncio
async def test_get_in_radius_calls_repo_with_pagination(db_with_companies_repo, pagination_input):
    """Проверяет корректное "прокидывание" пагинации в get_in_radius."""
    service = CompaniesService(db=db_with_companies_repo)

    await service.get_in_radius(
        pagination=pagination_input,
        lon=27.56,
        lat=53.90,
        radius_m=5000,
    )

    db_with_companies_repo.companies.get_in_radius.assert_awaited_once_with(
        lon=27.56,
        lat=53.90,
        radius_m=5000,
        limit=10,
        offset=10,
    )


@pytest.mark.asyncio
async def test_get_by_name_calls_repo_with_pagination(db_with_companies_repo, pagination_input):
    """Проверяет корректное "прокидывание" пагинации в get_by_name."""
    service = CompaniesService(db=db_with_companies_repo)

    await service.get_by_name(pagination=pagination_input, name="Рог")

    db_with_companies_repo.companies.get_by_name.assert_awaited_once_with(
        name="Рог",
        limit=10,
        offset=10,
    )
