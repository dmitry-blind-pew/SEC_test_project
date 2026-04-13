import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "params",
    [
        {"lon": 27.56, "lat": 53.90, "radius_m": 0},
        {"lon": 27.56, "lat": 53.90, "radius_m": -1},
    ],
)
async def test_radius_query_validation_422(api_client: AsyncClient, params: dict):
    """Проверяет валидацию радиуса: значения <= 0 должны возвращать 422 ошибку."""
    r = await api_client.get("/api/v1/companies/search/by-radius", params=params)
    assert r.status_code == 422


@pytest.mark.parametrize(
    "params",
    [
        {"lon": 200, "lat": 53.90, "radius_m": 1000},
        {"lon": 27.56, "lat": 100, "radius_m": 1000},
    ],
)
async def test_radius_lon_lat_validation_422(api_client: AsyncClient, params: dict):
    """Проверяет валидацию долготы и широты вне допустимых границ для поиска в радиусе."""
    r = await api_client.get("/api/v1/companies/search/by-radius", params=params)
    assert r.status_code == 422
