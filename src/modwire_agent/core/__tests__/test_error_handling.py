from django.test import RequestFactory, TestCase
from pydantic import BaseModel
from pydantic import ValidationError as PydanticValidationError

from modwire_agent.core.api import api
from modwire_agent.core.error_handling import GENERIC_ERROR_MESSAGE


class NinjaExtraValidationScenarios(TestCase):
    def test_masks_ninja_extra_validation_errors_without_error_logging(self) -> None:
        with self.assertNoLogs("modwire_agent.core.error_handling", level="ERROR"):
            response = self.client.get("/api/records/search/text")

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.json(), {"detail": GENERIC_ERROR_MESSAGE})

    def test_projects_ninja_extra_validation_errors_as_siren(self) -> None:
        response = self.client.get("/siren/records/search/text")

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response["Content-Type"], "application/vnd.siren+json")
        self.assertEqual(response.json()["properties"], {"detail": GENERIC_ERROR_MESSAGE})

    def test_masks_pydantic_response_serialization_errors_without_error_logging(self) -> None:
        class LegacyRecord(BaseModel):
            title: str

        with self.assertRaises(PydanticValidationError) as captured:
            LegacyRecord.model_validate({"title": None})

        with self.assertNoLogs("modwire_agent.core.error_handling", level="ERROR"):
            response = api.on_exception(RequestFactory().get("/api/records"), captured.exception)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(response.content, b'{"detail": "Request failed."}')
