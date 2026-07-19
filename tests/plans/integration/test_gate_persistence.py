from modwire.plans.adapters.django.models import GateSatisfactionModel

from ..functional.api import PlanApiTestCase


class GatePersistenceScenarios(PlanApiTestCase):
    def test_gate_evidence_is_idempotent_but_never_overwritten(self) -> None:
        definition = self.definition({
            "gates": [{"id": "reviewed", "stage_id": "frame", "evidence_schema": {"type": "object", "required": ["by"], "properties": {"by": {"type": "string"}}}}]
        })
        published = self.publish(definition)
        run = self.start(published.json()["id"], {"goal": "replace scaffoldings"})

        first = self.satisfy(run.json()["id"], "reviewed", {"by": "architect"})
        retry = self.satisfy(run.json()["id"], "reviewed", {"by": "architect"})
        conflict = self.satisfy(run.json()["id"], "reviewed", {"by": "owner"})

        evidence = GateSatisfactionModel.objects.get(plan_run_id=run.json()["id"], gate_id="reviewed")
        self.assertEqual(first.status_code, 204)
        self.assertEqual(retry.status_code, 204)
        self.assertEqual(conflict.status_code, 422)
        self.assertEqual(evidence.evidence, {"by": "architect"})
        self.assertEqual(GateSatisfactionModel.objects.filter(plan_run_id=run.json()["id"], gate_id="reviewed").count(), 1)

    def test_gate_evidence_is_isolated_to_its_run(self) -> None:
        definition = self.definition({
            "gates": [{"id": "reviewed", "stage_id": "frame", "evidence_schema": {"type": "object", "required": ["by"]}}]
        })
        published = self.publish(definition)
        first_run = self.start(published.json()["id"], {"goal": "first"})
        second_run = self.start(published.json()["id"], {"goal": "second"})

        satisfied = self.satisfy(first_run.json()["id"], "reviewed", {"by": "architect"})
        first_advanced = self.submit(first_run.json()["id"], {"decision": "preserve seam"})
        second_blocked = self.submit(second_run.json()["id"], {"decision": "preserve seam"})

        self.assertEqual(satisfied.status_code, 204)
        self.assertEqual(first_advanced.status_code, 200)
        self.assertEqual(second_blocked.status_code, 422)
