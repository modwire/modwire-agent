from modwire.plans.adapters.django.models import PlanDefinitionModel

from ..functional.api import PlanApiTestCase


class DefinitionPersistenceScenarios(PlanApiTestCase):
    def test_malformed_schema_rejects_the_definition_before_persistence(self) -> None:
        definition = self.definition({
            "stages": [
                {
                    "id": "frame",
                    "input_schema": {"type": "not-a-json-schema-type"},
                    "submission_schema": {"type": "object"},
                }
            ],
            "transitions": [],
        })

        response = self.publish(definition)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(PlanDefinitionModel.objects.exists())
