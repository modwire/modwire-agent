from dirty_equals import IsList, IsPartialDict, IsStr
from django.test import TestCase


class ScaffoldingPreviewApiTests(TestCase):
    def converge(self):
        return self.client.post(
            "/api/scaffoldings/converge",
            data={
                "language_id": "python",
                "name": "preview-safe",
                "description": "A scaffolding used to exercise the preview API.",
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
                    {
                        "relative_path": "{{ package_name }}/main.py",
                        "file_content": "print('{{ package_name }}')\n",
                    }
                ],
                "dry_run": False,
            },
            content_type="application/json",
        )

    def test_convergence_returns_the_identifier_needed_by_the_remaining_public_api(self) -> None:
        response = self.converge()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            IsPartialDict(id=IsStr(min_length=1), name="preview-safe", dry_run=False, changed=True),
        )

    def preview(self, payload: dict[str, object]):
        convergence = self.converge()
        self.assertEqual(convergence.status_code, 200)
        scaffolding_id = convergence.json()["id"]
        return self.client.post(
            f"/api/scaffoldings/{scaffolding_id}/preview",
            data=payload,
            content_type="application/json",
        )

    def test_returns_structured_errors_for_unknown_missing_and_wrongly_typed_values(self) -> None:
        response = self.preview({"values": {"unknown": "value", "package_name": 42}})

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            IsPartialDict(
                errors=IsList(
                    IsPartialDict(code="unknown_variable", details=IsPartialDict(field="unknown")),
                    IsPartialDict(code="invalid_variable_type", details=IsPartialDict(field="package_name")),
                )
            ),
        )

        missing = self.preview({"values": {}})

        self.assertEqual(missing.status_code, 422)
        self.assertEqual(
            missing.json(),
            IsPartialDict(
                errors=IsList(IsPartialDict(code="required_variable", details=IsPartialDict(field="package_name")))
            ),
        )

    def test_renders_only_validated_values_and_preserves_template_metadata(self) -> None:
        convergence = self.converge()
        self.assertEqual(convergence.status_code, 200)
        scaffolding_id = convergence.json()["id"]
        bundle = self.client.get(f"/api/scaffoldings/{scaffolding_id}/bundle")
        self.assertEqual(bundle.status_code, 200)

        response = self.client.post(
            f"/api/scaffoldings/{scaffolding_id}/preview",
            data={"values": {"package_name": "modwire"}},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            IsPartialDict(
                files=IsList(
                    IsPartialDict(
                        template_id=bundle.json()["templates"][0]["id"],
                        path="modwire/main.py",
                        source="print('modwire')\n",
                        language="python",
                        write_mode="managed",
                    )
                )
            ),
        )

    def test_rejects_an_override_that_targets_another_scaffolding(self) -> None:
        response = self.preview(
            {
                "values": {"package_name": "modwire"},
                "template_overrides": [
                    {
                        "template_id": "not-a-template-from-this-scaffolding",
                        "relative_path": "unsafe.py",
                        "file_content": "print('unsafe')",
                    }
                ],
            }
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            IsPartialDict(
                errors=IsList(
                    IsPartialDict(
                        code="invalid_template_override",
                        details=IsPartialDict(template_id="not-a-template-from-this-scaffolding"),
                    )
                )
            ),
        )

    def test_rejects_a_template_override_that_renders_outside_the_package(self) -> None:
        convergence = self.converge()
        self.assertEqual(convergence.status_code, 200)
        scaffolding_id = convergence.json()["id"]
        bundle = self.client.get(f"/api/scaffoldings/{scaffolding_id}/bundle")
        self.assertEqual(bundle.status_code, 200)

        response = self.client.post(
            f"/api/scaffoldings/{scaffolding_id}/preview",
            data={
                "values": {"package_name": "modwire"},
                "template_overrides": [
                    {
                        "template_id": bundle.json()["templates"][0]["id"],
                        "relative_path": "../../escape.py",
                        "file_content": "print('unsafe')",
                    }
                ],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(
            response.json(),
            IsPartialDict(
                errors=IsList(
                    IsPartialDict(
                        code="invalid_rendered_path",
                        details=IsPartialDict(template_id=bundle.json()["templates"][0]["id"]),
                    )
                )
            ),
        )
