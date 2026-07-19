import pytest

from modwire.tokens.adapters.django.models.api_key import ApiKey


@pytest.fixture
def api_key(db):
    _, key = ApiKey.generate("endpoint-test")
    return key


@pytest.fixture
def auth(api_key):
    return {"HTTP_APIKEY": api_key}
