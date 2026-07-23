from ..api import PlanApiTestCase


class RunIntegrityAttacks(PlanApiTestCase):
    def test_rejects_input_and_submission_that_violate_declared_contracts(self) -> None:
        published = self.publish(self.definition({}))

        invalid_start = self.start(published.json()["id"], {"goal": 42})
        run = self.start(published.json()["id"], {"goal": "replace scaffoldings"})
        invalid_submission = self.submit(run.json()["id"], {"decision": 42})
        valid_submission = self.submit(run.json()["id"], {"decision": "preserve seam"})
        completed = self.submit(valid_submission.json()["id"], {"outcome": "ready"})
        duplicate_submission = self.submit(completed.json()["id"], {"outcome": "again"})

        self.assertEqual(invalid_start.status_code, 422)
        self.assertEqual(invalid_submission.status_code, 422)
        self.assertEqual(valid_submission.status_code, 200)
        self.assertEqual(completed.status_code, 200)
        self.assertEqual(duplicate_submission.status_code, 422)

    def test_rejects_gate_evidence_outside_its_stage_or_schema(self) -> None:
        definition = self.definition(
            {
                "gates": [
                    {
                        "id": "reviewed",
                        "stage_id": "frame",
                        "evidence_schema": {
                            "type": "object",
                            "required": ["by"],
                            "properties": {"by": {"type": "string"}},
                        },
                    }
                ]
            }
        )
        published = self.publish(definition)
        run = self.start(published.json()["id"], {"goal": "replace scaffoldings"})

        malformed = self.satisfy(run.json()["id"], "reviewed", {"by": 3})
        valid = self.satisfy(run.json()["id"], "reviewed", {"by": "architect"})
        advanced = self.submit(run.json()["id"], {"decision": "preserve seam"})
        wrong_stage = self.satisfy(advanced.json()["id"], "reviewed", {"by": "architect"})

        self.assertEqual(malformed.status_code, 422)
        self.assertEqual(valid.status_code, 204)
        self.assertEqual(wrong_stage.status_code, 422)

    def test_rejects_unknown_gate_and_operation_as_client_errors(self) -> None:
        published = self.publish(self.definition({}))
        run = self.start(published.json()["id"], {"goal": "replace scaffoldings"})

        unknown_gate = self.satisfy(run.json()["id"], "missing", {"by": "architect"})
        unknown_operation = self.execute_operation(run.json()["id"], "missing")

        self.assertEqual(unknown_gate.status_code, 422)
        self.assertEqual(unknown_operation.status_code, 422)
