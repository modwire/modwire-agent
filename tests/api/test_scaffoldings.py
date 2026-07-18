import pytest

from .support import ScaffoldingResourceFactory

pytestmark = pytest.mark.django_db


class TestScaffoldingAggregate(ScaffoldingResourceFactory):
    def test_schema_bundle_preview_and_convergence_are_siren_endpoint_resources(self, client, auth):
        api = self.api(client, auth)
        scaffolding = self.create_scaffolding(api)
        variable = self.create_variable(api, scaffolding["id"])
        template = self.create_template(api, scaffolding["id"])

        self.siren(api.get(f"/api/scaffoldings/{scaffolding['id']}")).assert_actions(
            [
                "get_scaffolding",
                "get_scaffolding_schema",
                "get_scaffolding_bundle",
                "preview_scaffolding",
            ]
        )

        schema = self.siren(api.get(f"/api/scaffoldings/{scaffolding['id']}/schema")).assert_classes(
            "scaffolding-schema"
        )
        assert schema.links["self"].endswith(f"/api/scaffoldings/{scaffolding['id']}/schema")
        assert "project_name" in schema.properties["properties"]
        assert schema.properties["required"] == ["project_name"]

        bundle = self.siren(api.get(f"/api/scaffoldings/{scaffolding['id']}/bundle")).assert_classes(
            "scaffolding-bundle"
        )
        assert bundle.links["self"].endswith(f"/api/scaffoldings/{scaffolding['id']}/bundle")
        assert bundle.properties["variables"][0]["id"] == variable["id"]
        assert bundle.properties["templates"][0]["id"] == template["id"]

        preview = self.siren(
            api.post(
                f"/api/scaffoldings/{scaffolding['id']}/preview",
                {"values": {"project_name": "Ada"}, "template_overrides": []},
            )
        ).assert_classes("scaffolding-preview")
        assert preview.properties["files"][0]["path"] == "README.md"
        assert "Ada" in preview.properties["files"][0]["source"]
        assert preview.links["self"].endswith(f"/api/scaffoldings/{scaffolding['id']}/preview")

        convergence = self.siren(
            api.post(
                "/api/scaffoldings/converge",
                {
                    "language_id": "python",
                    "name": "Endpoint Convergence",
                    "description": "Dry-run convergence through endpoint tests.",
                    "variables": [
                        {
                            "name": "project_name",
                            "type": "str",
                            "description": "Project display name.",
                            "default_value": "World",
                            "required": True,
                        }
                    ],
                    "templates": [
                        {
                            "relative_path": "README.md",
                            "file_content": "# {{ project_name }}",
                            "write_mode": "managed",
                        }
                    ],
                    "dry_run": True,
                },
            )
        ).assert_classes("scaffolding-convergence")
        assert convergence.properties["dry_run"] is True
        assert convergence.properties["plan"]["scaffolding"] == "create"
        assert convergence.links["self"].endswith("/api/scaffoldings/converge")

        assert api.delete(f"/api/templates/{template['id']}").content == b""
        assert api.delete(f"/api/variables/{variable['id']}").content == b""
        assert api.delete(f"/api/scaffoldings/{scaffolding['id']}").content == b""

    def test_preview_reports_required_variable_failures_as_endpoint_problem_shape(self, client, auth):
        api = self.api(client, auth)
        scaffolding = self.create_scaffolding(api, "Preview Failure")
        self.create_variable(api, scaffolding["id"], required=True)
        self.create_template(api, scaffolding["id"])

        document = self.problem(
            api.post(
                f"/api/scaffoldings/{scaffolding['id']}/preview",
                {"values": {}, "template_overrides": []},
                expected=422,
            )
        )

        assert "required_variable" in document.body["detail"]


class TestScaffoldingCollection(ScaffoldingResourceFactory):
    def test_scaffolding_collection_advertises_create_and_converge_controls(self, client, auth):
        document = self.siren(self.api(client, auth).get("/api/scaffoldings")).assert_classes(
            "collection",
            "scaffolding",
        )

        document.assert_actions(["list_scaffoldings", "create_scaffolding", "converge_scaffolding"])

    def test_unknown_language_is_rejected_by_create_endpoint(self, client, auth):
        document = self.problem(
            self.api(client, auth).post(
                "/api/scaffoldings",
                {
                    "language_id": "brainfuck",
                    "name": "Impossible",
                    "description": "Unknown language.",
                },
                expected=422,
            )
        )

        assert document.body["status"] == 422
