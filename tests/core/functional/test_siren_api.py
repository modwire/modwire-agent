import json
from urllib.parse import urlparse

from django.test import TestCase

from modwire.core.api import api
from modwire.core.siren import facade


class SirenApiTests(TestCase):
    def test_advertises_and_executes_a_tag_write_action(self) -> None:
        document = self.client.get("/siren/").json()

        action = next(action for action in document["actions"] if action["name"] == "create_tag")
        self.assertEqual(action["href"], "http://testserver/siren/tags")
        self.assertEqual(action["method"], "POST")
        self.assertEqual(action["type"], "application/json")
        self.assertEqual([(field["name"], field["required"]) for field in action["fields"]], [("name", True)])

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

    def test_advertises_and_executes_a_section_write_action(self) -> None:
        document = self.client.get("/siren/sections").json()

        action = next(action for action in document["actions"] if action["name"] == "create_section")
        self.assertEqual(action["href"], "http://testserver/siren/sections")
        self.assertEqual(action["method"], "POST")
        self.assertEqual(action["type"], "application/json")
        self.assertEqual(
            [(field["name"], field["required"]) for field in action["fields"]],
            [("title", True), ("allowed_kinds", True)],
        )

        response = self.client.post(
            urlparse(action["href"]).path,
            data=json.dumps({"title": "Architecture", "allowed_kinds": ["rule"]}),
            content_type=action["type"],
            headers={"X-Actor-Id": "test-agent", "X-Actor-Type": "agent"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["section"])
        self.assertEqual(response.json()["properties"]["title"], "Architecture")

    def test_discovers_every_documented_rest_operation(self) -> None:
        documented = {
            operation["operationId"]
            for path_item in api.get_openapi_schema()["paths"].values()
            for operation in path_item.values()
            if "operationId" in operation
        }

        self.assertEqual(facade.operation_ids, documented)

    def test_serves_a_siren_root_derived_from_the_rest_contract(self) -> None:
        response = self.client.get("/siren/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["api", "entry-point"])
        self.assertEqual(response.json()["properties"]["title"], "Modwire API")
        self.assertEqual(
            response.json()["links"],
            [
                {"rel": ["self"], "href": "http://testserver/siren/"},
                {"rel": ["tag"], "href": "http://testserver/siren/tags"},
                {"rel": ["language"], "href": "http://testserver/siren/languages"},
                {"rel": ["section"], "href": "http://testserver/siren/sections"},
            ],
        )
        actions = {action["name"]: action for action in response.json()["actions"]}
        self.assertEqual(
            set(actions),
            {
                "create_api_key",
                "converge_scaffolding",
                "create_section",
                "create_tag",
                "list_published_records",
                "publish_plan_definition",
                "start_plan_run",
            },
        )
        self.assertEqual(
            actions["list_published_records"],
            {
                "name": "list_published_records",
                "href": "http://testserver/siren/records",
                "method": "GET",
                "fields": [{"name": "tag", "type": "array", "required": True}],
            },
        )

        for link in response.json()["links"]:
            linked_response = self.client.get(urlparse(link["href"]).path)

            self.assertEqual(linked_response.status_code, 200)
            self.assertEqual(linked_response["Content-Type"], "application/vnd.siren+json")

    def test_forwards_a_rest_mutation_and_projects_its_siren_entity(self) -> None:
        response = self.client.post(
            "/siren/sections",
            data={"title": "Architecture", "allowed_kinds": ["rule"]},
            content_type="application/json",
            headers={"X-Actor-Id": "test-agent", "X-Actor-Type": "agent"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["section"])
        self.assertEqual(response.json()["properties"]["title"], "Architecture")
        self.assertIn("get_section_details", {action["name"] for action in response.json()["actions"]})

    def test_projects_collections_with_embedded_entities_and_transport_actions(self) -> None:
        response = self.client.get("/siren/languages")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["collection", "language"])
        self.assertTrue(response.json()["entities"])
        self.assertEqual(response.json()["entities"][0]["rel"], ["item"])
        self.assertIn("id", response.json()["entities"][0]["properties"])
        self.assertIn({"rel": ["self"], "href": "http://testserver/siren/languages"}, response.json()["links"])
        self.assertIn(
            {"name": "list_languages", "href": "http://testserver/siren/languages", "method": "GET"},
            response.json()["actions"],
        )

    def test_represents_an_openapi_command_not_in_the_resource_graph(self) -> None:
        response = self.client.post(
            "/siren/scaffoldings/converge",
            data={
                "language_id": "python",
                "name": "starter",
                "description": "A starter project.",
                "variables": [],
                "templates": [],
                "dry_run": True,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["command"])
        self.assertTrue(response.json()["properties"]["dry_run"])

    def test_projects_api_errors_as_siren_documents_without_losing_the_error_payload(self) -> None:
        response = self.client.get("/siren/languages/not-a-language")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["error"])
        self.assertEqual(response.json()["properties"], {"detail": "Request failed."})
        self.assertEqual(
            response.json()["links"], [{"rel": ["self"], "href": "http://testserver/siren/languages/not-a-language"}]
        )
