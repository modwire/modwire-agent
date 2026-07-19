from ..api import PlanApiTestCase


class GateControlScenarios(PlanApiTestCase):
    def test_all_stage_gates_must_be_satisfied_before_advancing(self) -> None:
        definition = self.definition({
            "gates": [
                {"id": "reviewed", "stage_id": "frame", "evidence_schema": {"type": "object", "required": ["by"]}},
                {"id": "approved", "stage_id": "frame", "evidence_schema": {"type": "object", "required": ["by"]}},
            ]
        })
        published = self.publish(definition)
        run = self.start(published.json()["id"], {"goal": "replace scaffoldings"})

        initially_blocked = self.submit(run.json()["id"], {"decision": "preserve seam"})
        reviewed = self.satisfy(run.json()["id"], "reviewed", {"by": "architect"})
        still_blocked = self.submit(run.json()["id"], {"decision": "preserve seam"})
        approved = self.satisfy(run.json()["id"], "approved", {"by": "owner"})
        advanced = self.submit(run.json()["id"], {"decision": "preserve seam"})

        self.assertEqual(initially_blocked.status_code, 422)
        self.assertEqual(reviewed.status_code, 204)
        self.assertEqual(still_blocked.status_code, 422)
        self.assertEqual(approved.status_code, 204)
        self.assertEqual(advanced.status_code, 200)
        self.assertEqual(advanced.json()["current_stage_id"], "decide")
