import pytest
from httpx import AsyncClient

from tests.integration_tests.constants import PROTECTED_GET_CASES


@pytest.mark.parametrize("path,params", PROTECTED_GET_CASES)
async def test_ok_with_valid_api_key(api_client: AsyncClient, path: str, params: dict):
    r = await api_client.get(path, params=params)
    assert r.status_code == 200
