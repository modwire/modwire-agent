from modwire.plans.adapters.django.models import PlanRunModel

from ..functional.api import PlanApiTestCase


class DefinitionVersioningScenarios(PlanApiTestCase):
    def test_publishes_immutable_versions_and_runs_pin_their_definition(self) -> None:
        first = self.publish(self.definition({}))
        started = self.start(first.json()["id"], {"goal": "replace scaffoldings"})
        second = self.publish(self.definition({
            "stages": [
                {
                    "id": "frame",
                    "input_schema": {"type": "object", "required": ["different_goal"]},
                    "submission_schema": {"type": "object", "required": ["outcome"]},
                }
            ],
            "transitions": [],
        }))

        continued = self.submit(started.json()["id"], {"decision": "preserve seam"})
        run = PlanRunModel.objects.get(identifier=started.json()["id"])
        rejected_new_run = self.start(second.json()["id"], {"goal": "replace scaffoldings"})

        self.assertEqual(first.json()["version"], 1)
        self.assertEqual(second.json()["version"], 2)
        self.assertEqual(continued.status_code, 200)
        self.assertEqual(continued.json()["current_stage_id"], "decide")
        self.assertEqual(str(run.definition_id), first.json()["id"])
        self.assertEqual(run.definition_version, 1)
        self.assertEqual(rejected_new_run.status_code, 422)
