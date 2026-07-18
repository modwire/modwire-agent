import pytest

from .support import EndpointAssertions

pytestmark = pytest.mark.django_db


class TestApiKeyResource(EndpointAssertions):
    def test_api_key_lifecycle_is_exposed_through_endpoints(self, client, auth):
        api = self.api(client, auth)
        child = self.siren(api.post("/api/api_keys", {"name": "child-key"})).properties

        assert child["name"] == "child-key"
        assert "key" in child

        api_keys = self.siren(api.get("/api/api_keys")).assert_classes("collection", "api-key")
        api_keys.assert_actions(["list_api_keys", "create_api_key"])
        assert any(entity.get("properties", {}).get("id") == child["id"] for entity in api_keys.embedded("api-key"))

        patched = self.siren(api.patch(f"/api/api_keys/{child['id']}", {"name": "renamed-key"}))
        assert patched.properties["name"] == "renamed-key"

        self.siren(api.get(f"/api/api_keys/{child['id']}")).assert_classes("api-key").assert_actions(
            ["get_api_key", "partial_update_api_key", "delete_api_key"]
        )
        assert api.delete(f"/api/api_keys/{child['id']}").content == b""

    def test_deleted_api_key_cannot_be_used_to_pass_the_auth_gate(self, client, auth):
        api = self.api(client, auth)
        child = self.siren(api.post("/api/api_keys", {"name": "revoked-key"})).properties
        child_secret = child["key"]

        api.delete(f"/api/api_keys/{child['id']}")

        document = self.problem(
            self.api(client, {"HTTP_APIKEY": child_secret}).get("/api/", expected=401)
        )
        assert document.body["status"] == 401
