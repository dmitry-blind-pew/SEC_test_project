import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "path,expected_status,expected_body",
    [
        ("/api/v1/buildings/999999/companies", 200, []),
        ("/api/v1/activities/999999/companies", 200, []),
        ("/api/v1/activities/999999/companies/tree", 200, []),
    ],
)
async def test_unknown_building_or_activity_returns_empty_company_list(
    api_client: AsyncClient,
    path: str,
    expected_status: int,
    expected_body: list,
):
    """Проверяет, что неизвестные building/activity id дают пустой список компаний."""
    r = await api_client.get(path)
    assert r.status_code == expected_status
    assert r.json() == expected_body
