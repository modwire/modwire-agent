from django.test import TestCase


class PlanRunScenarios(TestCase):
    def test_runs_a_published_two_stage_definition(self) -> None:
        definition = self.client.post("/api/plans/definitions", data=self._definition(), content_type="application/json")
        run = self.client.post("/api/plans/runs", data={"definition_id": definition.json()["id"], "initial_input": {"goal": "replace scaffoldings"}}, content_type="application/json")
        blocked = self.client.post(f"/api/plans/runs/{run.json()['id']}/submissions", data={"payload": {"decision": "preserve public seam"}}, content_type="application/json")
        gate = self.client.post(f"/api/plans/runs/{run.json()['id']}/gates/reviewed/satisfactions", data={"evidence": {"approved_by": "architect"}}, content_type="application/json")
        advanced = self.client.post(f"/api/plans/runs/{run.json()['id']}/submissions", data={"payload": {"decision": "preserve public seam"}}, content_type="application/json")
        completed = self.client.post(f"/api/plans/runs/{run.json()['id']}/submissions", data={"payload": {"outcome": "records is ready"}}, content_type="application/json")

        self.assertEqual(definition.status_code, 201)
        self.assertEqual(run.json()["current_stage_id"], "frame")
        self.assertEqual(blocked.status_code, 422)
        self.assertEqual(gate.status_code, 204)
        self.assertEqual(advanced.json()["current_stage_id"], "decide")
        self.assertEqual(completed.json()["status"], "complete")

    def _definition(self) -> dict[str, object]:
        return {
            "name": "replacement",
            "start_stage_id": "frame",
            "stages": [
                {"id": "frame", "input_schema": {"type": "object", "required": ["goal"], "properties": {"goal": {"type": "string"}}}, "submission_schema": {"type": "object", "required": ["decision"], "properties": {"decision": {"type": "string"}}}},
                {"id": "decide", "input_schema": {"type": "object", "required": ["decision"], "properties": {"decision": {"type": "string"}}}, "submission_schema": {"type": "object", "required": ["outcome"], "properties": {"outcome": {"type": "string"}}}},
            ],
            "transitions": [{"source_stage_id": "frame", "target_stage_id": "decide"}],
            "gates": [{"id": "reviewed", "stage_id": "frame", "evidence_schema": {"type": "object", "required": ["approved_by"], "properties": {"approved_by": {"type": "string"}}}}],
            "operations": [],
        }
