import pytest

from .support import EndpointAssertions

pytestmark = pytest.mark.django_db


class TestApiGate(EndpointAssertions):
    def test_root_rejects_missing_api_key_with_problem_document(self, client):
        document = self.problem(self.api(client).get("/api/", expected=401))

        assert document.body["status"] == 401

    def test_root_rejects_invalid_api_key_with_problem_document(self, client):
        document = self.problem(
            self.api(client, {"HTTP_APIKEY": "invalid"}).get("/api/", expected=401)
        )

        assert document.body["title"] == "Unauthorized"


class TestApiDiscovery(EndpointAssertions):
    def test_root_and_openapi_describe_the_same_siren_api(self, client, auth):
        api = self.api(client, auth)

        root = self.siren(api.get("/api/")).assert_classes("api")
        openapi = api.get("/api/openapi.json").json()

        assert root.properties["version"] == openapi["info"]["version"]
        assert {"self", "records", "scaffoldings", "browser", "service-desc"}.issubset(root.links)
        assert "record-search" not in root.links
        assert "scaffolding-convergence" not in root.links
        assert {"SirenEntity", "Problem"}.issubset(openapi["components"]["schemas"])
        assert openapi["paths"]["/api/records/{record_slug}"]["x-siren-resource"]["name"] == "record"

    def test_root_links_honor_https_forwarded_by_the_deployment_proxy(self, client, auth, settings):
        settings.ALLOWED_HOSTS = ["modwire.example"]

        document = self.siren(
            self.api(client, auth).get(
                "/api/",
                HTTP_HOST="modwire.example",
                HTTP_X_FORWARDED_PROTO="https",
            )
        )

        assert document.links["self"].startswith("https://modwire.example/")
        assert document.links["service-desc"] == "https://modwire.example/api/openapi.json"
