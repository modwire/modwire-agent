import pytest
from oa.client import Client


@pytest.fixture
def api_client(live_server):
    with Client(base_url=live_server.url, raise_on_unexpected_status=True) as client:
        yield client
