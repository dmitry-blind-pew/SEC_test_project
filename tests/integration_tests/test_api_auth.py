import pytest
from httpx import AsyncClient

from tests.integration_tests.constants import PROTECTED_GET_CASES


@pytest.mark.parametrize("path,params", PROTECTED_GET_CASES)
@pytest.mark.parametrize(
    "client_fixture",
    ["api_client_wrong_key", "api_client_no_key"],
    indirect=True,
)
async def test_forbidden_for_invalid_or_missing_api_key(
    client_fixture: AsyncClient,
    path: str,
    params: dict,
):
    r = await client_fixture.get(path, params=params)
    assert r.status_code == 403
