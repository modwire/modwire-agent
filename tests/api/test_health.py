import pytest

from .support import EndpointAssertions

pytestmark = pytest.mark.django_db


class TestHealthEndpoint(EndpointAssertions):
    def test_health_reports_database_readiness(self, client):
        response = self.api(client).get("/health/?format=json")

        assert response.json() == {"Database(alias='default')": "OK"}
