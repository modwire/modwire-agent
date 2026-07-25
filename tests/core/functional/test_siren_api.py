import json
from urllib.parse import urlparse

from django.test import TestCase


class SirenApiTests(TestCase):
    def test_serves_a_siren_root_derived_from_the_rest_contract(self) -> None:
        response = self.client.get("/siren/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["api", "entry-point"])
        self.assertEqual(response.json()["properties"]["title"], "Modwire API")
        self.assertIn({"rel": ["collection"], "href": "http://testserver/siren/records"}, response.json()["links"])

    def test_advertises_and_executes_a_tag_write_action(self) -> None:
        document = self.client.get("/siren/tags").json()

        action = next(action for action in document["actions"] if action["name"] == "create_tag")
        self.assertEqual(action["href"], "http://testserver/siren/tags")
        self.assertEqual(action["method"], "POST")
        self.assertEqual(action["type"], "application/json")
        self.assertEqual([field["name"] for field in action["fields"]], ["name"])

        response = self.client.post(
            urlparse(action["href"]).path,
            data=json.dumps({"name": "Architecture"}),
            content_type=action["type"],
            headers={"X-Actor-Id": "test-agent", "X-Actor-Type": "agent"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["collection", "tag"])
        self.assertEqual(response.json()["entities"][0]["properties"]["name"], "architecture")

    def test_projects_api_errors_as_siren_documents(self) -> None:
        response = self.client.get("/siren/languages/not-a-language")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["error"])
        self.assertEqual(response.json()["properties"], {"detail": "Request failed."})
