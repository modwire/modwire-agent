import json
from urllib.parse import urlparse

from django.test import TestCase


class SirenApiTests(TestCase):
    def test_serves_a_siren_root_derived_from_the_rest_contract(self) -> None:
        response = self.client.get("/siren/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["api", "entry-point"])
        self.assertEqual(response.json()["title"], "Modwire API")
        self.assertEqual(response.json()["properties"]["title"], "Modwire API")
        self.assertIn(
            {"rel": ["collection"], "href": "http://testserver/siren/records", "title": "Records"},
            response.json()["links"],
        )

    def test_supplies_titles_for_collections_embedded_entities_and_errors(self) -> None:
        tags = self.client.get("/siren/tags").json()
        error = self.client.get("/siren/languages/not-a-language").json()

        self.assertEqual(tags["title"], "Tags")
        self.assertEqual(tags["links"][0]["title"], "Tags")
        self.assertEqual(error["title"], "Error")

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
        self.assertEqual(response.json()["title"], "Tags")
        self.assertEqual(response.json()["class"], ["collection", "tag"])
        self.assertEqual(response.json()["entities"][0]["title"], "architecture")
        self.assertEqual(response.json()["entities"][0]["properties"]["name"], "architecture")

    def test_preserves_list_field_shape_in_siren_actions(self) -> None:
        document = self.client.get("/siren/sections").json()

        action = next(action for action in document["actions"] if action["name"] == "create_section")

        self.assertEqual(action["fields"], [
            {"name": "title", "type": "text", "title": "Title"},
            {"name": "allowed_kinds", "type": "list", "title": "Allowed Kinds"},
        ])
        self.assertEqual(action["x-form"]["schema"]["required"], ["title", "allowed_kinds"])

    def test_projects_api_errors_as_siren_documents(self) -> None:
        response = self.client.get("/siren/languages/not-a-language")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["class"], ["error"])
        self.assertEqual(response.json()["properties"], {"detail": "Request failed."})

    def test_enforces_agent_and_user_roles_for_protected_mutations(self) -> None:
        tag_document = self.siren("get", "/siren/tags")
        missing_actor = self.call_action(tag_document, "create_tag", {"name": "Missing actor"}, status=422)
        self.assertEqual(missing_actor["class"], ["error"])
        self.assertEqual(
            missing_actor["properties"]["detail"], "Missing required actor headers: X-Actor-Id, X-Actor-Type."
        )
        self.call_action(tag_document, "create_tag", {"name": "User contribution"}, self.user_headers())

        sections_document = self.siren("get", "/siren/sections")
        section = self.call_action(
            sections_document, "create_section", {"title": "Rules", "allowed_kinds": ["rule"]}, self.agent_headers()
        )
        record = self.siren(
            "post",
            f"/siren/sections/{self.properties(section)['id']}/records",
            {"title": "Actor roles", "kind": "rule"},
            self.agent_headers(),
            status=201,
        )
        record_id = self.properties(record)["id"]
        proposal = self.siren(
            "post",
            f"/siren/records/{record_id}/content-proposals",
            {"markdown": "## Rules\n\nUse HTTP.\n\n## Verification\n\nExercise the public API."},
            self.agent_headers(),
            status=201,
        )
        rejected_agent_resolution = self.siren(
            "patch",
            f"/siren/content-proposals/{self.properties(proposal)['id']}",
            {"status": "accepted"},
            self.agent_headers(),
            status=422,
        )
        self.assertEqual(rejected_agent_resolution["class"], ["error"])
        self.assertEqual(
            rejected_agent_resolution["properties"]["detail"], "Only a user can resolve content proposals."
        )
        self.siren(
            "patch",
            f"/siren/content-proposals/{self.properties(proposal)['id']}",
            {"status": "accepted"},
            self.user_headers(),
        )

    def test_exercises_the_complete_records_hypermedia_flow(self) -> None:
        tag_document = self.siren("get", "/siren/tags")
        tag = self.call_action(tag_document, "create_tag", {"name": "Architecture"}, self.agent_headers())
        tag_id = self.properties(tag)["id"]

        sections_document = self.siren("get", "/siren/sections")
        section = self.call_action(
            sections_document, "create_section", {"title": "Rules", "allowed_kinds": ["rule"]}, self.agent_headers()
        )
        section_id = self.properties(section)["id"]

        record = self.siren(
            "post",
            f"/siren/sections/{section_id}/records",
            {"title": "Use HTTP", "kind": "rule"},
            self.agent_headers(),
            status=201,
        )
        record_id = self.properties(record)["id"]

        details = self.siren("get", f"/siren/records/{record_id}")
        self.call_action(details, "rename_record", {"title": "Use Hypermedia"}, self.agent_headers())
        self.call_action(
            details,
            "replace_record_content",
            {"markdown": "## Rules\n\nUse HTTP.\n\n## Verification\n\nExercise the public API."},
            self.agent_headers(),
        )

        proposal = self.siren(
            "post",
            f"/siren/records/{record_id}/content-proposals",
            {"markdown": "## Rules\n\nUse HTTP.\n\n## Verification\n\nExercise the public API."},
            self.agent_headers(),
            status=201,
        )
        proposal_id = self.properties(proposal)["id"]
        self.siren("get", f"/siren/records/{record_id}/content-proposals")
        self.siren(
            "patch",
            f"/siren/content-proposals/{proposal_id}",
            {"status": "accepted"},
            self.user_headers(),
        )
        self.siren("get", f"/siren/records/{record_id}/content-revisions")
        self.siren(
            "put", f"/siren/records/{record_id}/tags", {"tag_ids": [tag_id]}, self.agent_headers(), status=204
        )
        self.siren(
            "put", f"/siren/sections/{section_id}/placements", {"record_ids": [record_id]}, self.agent_headers()
        )
        self.call_action(details, "publish_record", None, self.agent_headers())
        self.siren("get", "/siren/records?tag=architecture")
        self.siren("get", "/siren/records/search/text?q=hypermedia")
        self.siren("get", "/siren/records/search/semantic?q=hypermedia")
        self.siren("get", f"/siren/sections/{section_id}")
        self.siren("get", "/siren/tags")
        self.siren("get", "/siren/sections")
        self.siren("delete", f"/siren/records/{record_id}", headers=self.agent_headers(), status=204)

    def test_exercises_languages_and_the_complete_plan_lifecycle(self) -> None:
        languages = self.siren("get", "/siren/languages")
        language_id = self.properties(languages)["id"]
        self.siren("get", f"/siren/languages/{language_id}")

        definition = self.siren("post", "/siren/plans/definitions", self.plan_definition(), status=201)
        definition_id = self.properties(definition)["id"]
        run = self.siren(
            "post",
            "/siren/plans/runs",
            {"definition_id": definition_id, "initial_input": {"goal": "test Siren"}},
            status=201,
        )
        run_id = self.properties(run)["id"]
        self.siren(
            "post", f"/siren/plans/runs/{run_id}/submissions", {"payload": {"decision": "continue"}}, status=422
        )
        self.siren(
            "post",
            f"/siren/plans/runs/{run_id}/gates/reviewed/satisfactions",
            {"evidence": {"by": "architect"}},
            status=204,
        )
        advanced = self.siren(
            "post", f"/siren/plans/runs/{run_id}/submissions", {"payload": {"decision": "continue"}}
        )
        self.assertEqual(self.properties(advanced)["current_stage_id"], "decide")
        completed = self.siren(
            "post", f"/siren/plans/runs/{run_id}/submissions", {"payload": {"outcome": "ready"}}
        )
        self.assertEqual(self.properties(completed)["status"], "complete")
        self.siren("post", f"/siren/plans/runs/{run_id}/operations/missing", status=422)

    def test_exercises_the_complete_scaffolding_hypermedia_flow(self) -> None:
        definition = {
            "language_id": "python",
            "name": "siren-preview",
            "description": "A Siren-accessible scaffolding.",
            "variables": [
                {
                    "name": "package_name",
                    "type": "str",
                    "description": "Python package name.",
                    "default_value": "",
                    "required": True,
                }
            ],
            "templates": [
                {"relative_path": "{{ package_name }}/main.py", "file_content": "print('{{ package_name }}')\n"}
            ],
            "dry_run": False,
        }
        convergence = self.siren("post", "/siren/scaffoldings/converge", definition)
        scaffolding_id = self.properties(convergence)["id"]
        self.siren("get", f"/siren/scaffoldings/{scaffolding_id}/schema")
        bundle = self.siren("get", f"/siren/scaffoldings/{scaffolding_id}/bundle")
        template_id = self.properties(bundle)["templates"][0]["id"]
        preview = self.siren(
            "post", f"/siren/scaffoldings/{scaffolding_id}/preview", {"values": {"package_name": "modwire"}}
        )
        self.assertEqual(self.properties(preview)["files"][0]["template_id"], template_id)
        self.siren("post", f"/siren/scaffoldings/{scaffolding_id}/preview", {"values": {}}, status=422)
        self.siren(
            "post",
            "/siren/scaffoldings/converge",
            {**definition, "name": "siren-dry-run", "variables": [], "templates": [], "dry_run": True},
        )

    def siren(
        self,
        method: str,
        path: str,
        payload: dict[str, object] | None = None,
        headers: dict[str, str] | None = None,
        status: int = 200,
    ) -> dict[str, object]:
        response = self.client.generic(
            method.upper(),
            path,
            data=json.dumps(payload) if payload is not None else None,
            content_type="application/json",
            headers=headers,
        )
        self.assertEqual(response.status_code, status)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        if status == 204:
            return {}
        return response.json()

    def call_action(
        self,
        document: dict[str, object],
        name: str,
        payload: dict[str, object] | None,
        headers: dict[str, str] | None = None,
        status: int | None = None,
    ) -> dict[str, object]:
        action = next(action for action in document["actions"] if action["name"] == name)
        return self.siren(
            action["method"],
            urlparse(action["href"]).path,
            payload,
            headers,
            status if status is not None else 201 if name in {"create_tag", "create_section"} else 200,
        )

    def properties(self, document: dict[str, object]) -> dict[str, object]:
        if entities := document.get("entities"):
            return entities[0]["properties"]
        return document["properties"]

    @staticmethod
    def agent_headers() -> dict[str, str]:
        return {"X-Actor-Id": "test-agent", "X-Actor-Type": "agent"}

    @staticmethod
    def user_headers() -> dict[str, str]:
        return {"X-Actor-Id": "test-user", "X-Actor-Type": "user"}

    @staticmethod
    def plan_definition() -> dict[str, object]:
        return {
            "name": "siren-plan",
            "start_stage_id": "frame",
            "stages": [
                {
                    "id": "frame",
                    "input_schema": {"type": "object", "required": ["goal"]},
                    "submission_schema": {"type": "object", "required": ["decision"]},
                },
                {
                    "id": "decide",
                    "input_schema": {"type": "object", "required": ["decision"]},
                    "submission_schema": {"type": "object", "required": ["outcome"]},
                },
            ],
            "transitions": [{"source_stage_id": "frame", "target_stage_id": "decide"}],
            "gates": [
                {
                    "id": "reviewed",
                    "stage_id": "frame",
                    "evidence_schema": {"type": "object", "required": ["by"]},
                }
            ],
            "operations": [],
        }
