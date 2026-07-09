import pytest
from oa.client import AuthenticatedClient

from tokens.models.api_key import ApiKey


@pytest.fixture
def api_client(live_server, transactional_db):
    _, key = ApiKey.generate("tests")
    with AuthenticatedClient(
        base_url=live_server.url,
        token=key,
        prefix="",
        auth_header_name="apikey",
        raise_on_unexpected_status=True,
    ) as client:
        yield client
