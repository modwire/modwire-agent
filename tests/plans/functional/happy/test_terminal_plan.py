from ..api import PlanApiTestCase


class TerminalPlanScenarios(PlanApiTestCase):
    def test_completes_a_single_terminal_stage(self) -> None:
        definition = self.definition({
            "stages": [
                {
                    "id": "frame",
                    "input_schema": {"type": "object", "required": ["goal"]},
                    "submission_schema": {"type": "object", "required": ["outcome"]},
                }
            ],
            "transitions": [],
        })

        published = self.publish(definition)
        run = self.start(published.json()["id"], {"goal": "replace scaffoldings"})
        completed = self.submit(run.json()["id"], {"outcome": "ready"})

        self.assertEqual(published.status_code, 201)
        self.assertEqual(run.status_code, 201)
        self.assertEqual(completed.status_code, 200)
        self.assertEqual(completed.json()["status"], "complete")
