from httpx import AsyncClient


async def test_company_not_found(api_client: AsyncClient) -> None:
    """Проверяет, что запрос несуществующей компании возвращает 404 ошибку."""
    r = await api_client.get("/api/v1/companies/999999")
    assert r.status_code == 404


async def test_rectangle_invalid_bounds(api_client: AsyncClient) -> None:
    """Проверяет, что некорректные границы области возвращают 422 ошибку."""
    r = await api_client.get(
        "/api/v1/companies/search/by-rectangle",
        params={
            "min_lon": 30.0,
            "min_lat": 53.0,
            "max_lon": 20.0,
            "max_lat": 54.0,
        },
    )
    assert r.status_code == 422
