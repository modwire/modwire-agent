from django.test import TestCase


class PlanApiTestCase(TestCase):
    def definition(self, overrides: dict[str, object]) -> dict[str, object]:
        value: dict[str, object] = {
            "name": "replacement",
            "start_stage_id": "frame",
            "stages": [
                {
                    "id": "frame",
                    "input_schema": {
                        "type": "object",
                        "required": ["goal"],
                        "properties": {"goal": {"type": "string"}},
                    },
                    "submission_schema": {
                        "type": "object",
                        "required": ["decision"],
                        "properties": {"decision": {"type": "string"}},
                    },
                },
                {
                    "id": "decide",
                    "input_schema": {
                        "type": "object",
                        "required": ["decision"],
                        "properties": {"decision": {"type": "string"}},
                    },
                    "submission_schema": {
                        "type": "object",
                        "required": ["outcome"],
                        "properties": {"outcome": {"type": "string"}},
                    },
                },
            ],
            "transitions": [{"source_stage_id": "frame", "target_stage_id": "decide"}],
            "gates": [],
            "operations": [],
        }
        value.update(overrides)
        return value

    def publish(self, definition: dict[str, object]):
        return self.client.post("/api/plans/definitions", data=definition, content_type="application/json")

    def start(self, definition_id: str, initial_input: dict[str, object]):
        return self.client.post(
            "/api/plans/runs",
            data={"definition_id": definition_id, "initial_input": initial_input},
            content_type="application/json",
        )

    def submit(self, run_id: str, payload: dict[str, object]):
        return self.client.post(
            f"/api/plans/runs/{run_id}/submissions", data={"payload": payload}, content_type="application/json"
        )

    def satisfy(self, run_id: str, gate_id: str, evidence: dict[str, object]):
        return self.client.post(
            f"/api/plans/runs/{run_id}/gates/{gate_id}/satisfactions",
            data={"evidence": evidence},
            content_type="application/json",
        )

    def execute_operation(self, run_id: str, operation_id: str):
        return self.client.post(f"/api/plans/runs/{run_id}/operations/{operation_id}", content_type="application/json")
