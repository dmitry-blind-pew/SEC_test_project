import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "path,params,expected_status,expected_body",
    [
        (
            "/api/v1/companies/search/by-radius",
            {"lon": 0.0, "lat": 0.0, "radius_m": 100},
            200,
            [],
        ),
        (
            "/api/v1/companies",
            {"name": "__no_such_company__xyz__"},
            200,
            [],
        ),
    ],
)
async def test_empty_search_returns_empty_list(
    api_client: AsyncClient,
    path: str,
    params: dict,
    expected_status: int,
    expected_body: list,
):
    """Проверяет, что поисковые запросы без совпадений возвращают пустой список."""
    r = await api_client.get(path, params=params)
    assert r.status_code == expected_status
    assert r.json() == expected_body
