from django.test import SimpleTestCase


class CorsScenarios(SimpleTestCase):
    def test_allows_local_development_preflight_requests(self) -> None:
        response = self.client.options(
            "/api/",
            HTTP_ORIGIN="http://localhost:5173",
            HTTP_ACCESS_CONTROL_REQUEST_METHOD="PATCH",
            HTTP_ACCESS_CONTROL_REQUEST_HEADERS="content-type,x-actor-id,x-actor-type",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Access-Control-Allow-Origin"], "*")
        self.assertIn("PATCH", response["Access-Control-Allow-Methods"])
        self.assertIn("content-type", response["Access-Control-Allow-Headers"])
        self.assertIn("x-actor-id", response["Access-Control-Allow-Headers"])
        self.assertIn("x-actor-type", response["Access-Control-Allow-Headers"])
