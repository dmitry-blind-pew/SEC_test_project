import pytest

from src.api.deps import verify_api_key
from src.core.config import settings
from src.core.domain_exc import ApiKeyInvalidException


def test_verify_api_key_accepts_valid_key():
    verify_api_key(settings.API_KEY)


@pytest.mark.parametrize("bad_key", [None, "", "wrong-key"])
def test_verify_api_key_rejects_invalid_key(bad_key):
    with pytest.raises(ApiKeyInvalidException):
        verify_api_key(bad_key)
