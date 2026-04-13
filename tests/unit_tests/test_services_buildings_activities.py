from typing import Any

import pytest

from src.services.activities import ActivitiesService
from src.services.buildings import BuildingsService


@pytest.mark.asyncio
async def test_buildings_service_get_by_building_id_calls_repo(
    db_with_companies_repo: Any, pagination_input: Any
) -> None:
    """Проверяет вызов get_filtered с id здания."""
    service = BuildingsService(db=db_with_companies_repo)

    await service.get_by_building_id(pagination=pagination_input, building_id=7)

    db_with_companies_repo.companies.get_filtered.assert_awaited_once_with(
        building_id=7,
        limit=10,
        offset=10,
    )


@pytest.mark.asyncio
async def test_activities_service_get_by_activity_calls_repo(
    db_with_companies_repo: Any, pagination_input: Any
) -> None:
    """Проверяет вызов get_by_activity с id деятельности."""
    service = ActivitiesService(db=db_with_companies_repo)

    await service.get_by_activity(pagination=pagination_input, activity_id=11)

    db_with_companies_repo.companies.get_by_activity.assert_awaited_once_with(
        activity_id=11,
        limit=10,
        offset=10,
    )


@pytest.mark.asyncio
async def test_activities_service_get_in_activity_calls_repo(
    db_with_companies_repo: Any, pagination_input: Any
) -> None:
    """Проверяет вызов get_in_activity с id деятельности."""
    service = ActivitiesService(db=db_with_companies_repo)

    await service.get_in_activity(pagination=pagination_input, activity_id=11)

    db_with_companies_repo.companies.get_in_activity.assert_awaited_once_with(
        activity_id=11,
        limit=10,
        offset=10,
    )
