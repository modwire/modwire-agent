from django.test import SimpleTestCase
from modwire_hex.django import DjangoNinja


class OpenApiScenarios(SimpleTestCase):
    def test_is_auth_free_and_does_not_expose_api_key_operations(self) -> None:
        schema = DjangoNinja.api().get_openapi_schema()
        response = self.client.post("/api/api_keys", data={"name": "removed"}, content_type="application/json")

        self.assertNotIn("/api_keys", schema["paths"])
        self.assertNotIn("securitySchemes", schema.get("components", {}))
        self.assertEqual(response.status_code, 404)

    def test_assigns_a_unique_operation_id_to_every_operation(self) -> None:
        schema = DjangoNinja.api().get_openapi_schema()
        operations = [
            operation
            for path_item in schema["paths"].values()
            for method, operation in path_item.items()
            if method.lower() in {"delete", "get", "patch", "post", "put"}
        ]
        operation_ids = [operation.get("operationId") for operation in operations]
        descriptions = [operation.get("description") for operation in operations]

        self.assertTrue(all(isinstance(operation_id, str) and operation_id for operation_id in operation_ids))
        self.assertEqual(len(operation_ids), len(set(operation_ids)))
        self.assertTrue(all(isinstance(description, str) and description for description in descriptions))
