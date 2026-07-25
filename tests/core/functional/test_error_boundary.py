from unittest.mock import patch

from django.test import TestCase

from modwire_agent.core.error_handling import GENERIC_ERROR_MESSAGE


class ErrorBoundaryScenarios(TestCase):
    def test_returns_a_domain_error_message(self) -> None:
        response = self.client.post(
            "/api/tags",
            data={"name": "invalid-actor"},
            content_type="application/json",
            headers={"X-Actor-Id": "test", "X-Actor-Type": "service"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": "Actor kind must be user or agent."})

    def test_masks_request_validation_details(self) -> None:
        response = self.client.post(
            "/api/tags",
            data={"name": "testing", "system": True},
            content_type="application/json",
            headers={"X-Actor-Id": "test", "X-Actor-Type": "agent"},
        )

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": GENERIC_ERROR_MESSAGE})

    def test_masks_missing_resource_details(self) -> None:
        response = self.client.get("/api/languages/not-a-language")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": GENERIC_ERROR_MESSAGE})

    def test_masks_and_logs_unexpected_errors_without_request_data(self) -> None:
        with (
            self.assertLogs("modwire_agent.core.error_handling", level="ERROR") as logs,
            patch(
                "modwire_agent.records.adapters.http.tag_api.CreateTag.execute",
                side_effect=RuntimeError("unexpected failure"),
            ),
        ):
            response = self.client.post(
                "/api/tags",
                data={"name": "do-not-log-me"},
                content_type="application/json",
                headers={"X-Actor-Id": "test", "X-Actor-Type": "agent"},
            )

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {"detail": GENERIC_ERROR_MESSAGE})
        output = "\n".join(logs.output)
        self.assertIn("unhandled_api_exception", output)
        self.assertIn("method", output)
        self.assertIn("POST", output)
        self.assertIn("path", output)
        self.assertIn(self.api_path("/api/tags"), output)
        self.assertNotIn("do-not-log-me", output)

    @staticmethod
    def api_path(path: str) -> str:
        return path
