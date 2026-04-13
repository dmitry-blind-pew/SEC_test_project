import json

import pytest
from fastapi.responses import JSONResponse

from src.core.domain_exc import (
    ApiKeyInvalidException,
    CompanyNotFoundException,
    InvalidRectangleBoundsException,
    ObjectNotFoundException,
)
from src.core.exc_handler import resolve_status_code, sectest_exception_handler


def test_resolve_status_code_maps_known_exceptions():
    assert resolve_status_code(ApiKeyInvalidException()) == 403
    assert resolve_status_code(ObjectNotFoundException()) == 404
    assert resolve_status_code(CompanyNotFoundException()) == 404
    assert resolve_status_code(InvalidRectangleBoundsException()) == 422


@pytest.mark.asyncio
async def test_sectest_exception_handler_returns_json_response():
    exc = CompanyNotFoundException()

    response = await sectest_exception_handler(request=None, exc=exc)

    assert isinstance(response, JSONResponse)
    assert response.status_code == 404
    assert json.loads(response.body) == {"detail": exc.detail}
