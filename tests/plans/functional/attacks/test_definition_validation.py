from ..api import PlanApiTestCase


class DefinitionValidationAttacks(PlanApiTestCase):
    def test_rejects_invalid_protocol_graphs(self) -> None:
        cases = {
            "blank-name": self.definition({"name": " "}),
            "unknown-start": self.definition({"start_stage_id": "missing"}),
            "duplicate-stage": self.definition({"stages": [*self.definition({})["stages"], self.definition({})["stages"][0]]}),
            "unknown-transition-target": self.definition({"transitions": [{"source_stage_id": "frame", "target_stage_id": "missing"}]}),
            "two-successors": self.definition({
                "stages": [*self.definition({})["stages"], {"id": "other", "input_schema": {"type": "object"}, "submission_schema": {"type": "object"}}],
                "transitions": [{"source_stage_id": "frame", "target_stage_id": "decide"}, {"source_stage_id": "frame", "target_stage_id": "other"}],
            }),
            "unreachable-stage": self.definition({
                "stages": [*self.definition({})["stages"], {"id": "other", "input_schema": {"type": "object"}, "submission_schema": {"type": "object"}}],
            }),
            "cycle": self.definition({
                "stages": [*self.definition({})["stages"], {"id": "review", "input_schema": {"type": "object"}, "submission_schema": {"type": "object"}}],
                "transitions": [{"source_stage_id": "frame", "target_stage_id": "decide"}, {"source_stage_id": "decide", "target_stage_id": "review"}, {"source_stage_id": "review", "target_stage_id": "decide"}],
            }),
            "incompatible-stage-contracts": self.definition({
                "stages": [
                    {"id": "frame", "input_schema": {"type": "object"}, "submission_schema": {"type": "object", "required": ["decision"], "properties": {"decision": {"type": "string"}}}},
                    {"id": "decide", "input_schema": {"type": "object", "required": ["approved"], "properties": {"approved": {"type": "boolean"}}}, "submission_schema": {"type": "object"}},
                ],
            }),
            "incompatible-optional-property": self.definition({
                "stages": [
                    {"id": "frame", "input_schema": {"type": "object"}, "submission_schema": {"type": "object", "required": ["decision"], "properties": {"decision": {"type": "string"}, "flag": {"type": "string"}}}},
                    {"id": "decide", "input_schema": {"type": "object", "required": ["decision"], "properties": {"decision": {"type": "string"}, "flag": {"type": "boolean"}}}, "submission_schema": {"type": "object"}},
                ],
            }),
            "orphaned-artifact": self.definition({
                "artifacts": [{"id": "contract", "producer_operation_id": "missing", "output_schema": {"type": "object"}}],
            }),
        }

        for name, definition in cases.items():
            with self.subTest(name=name):
                response = self.publish(definition)
                self.assertEqual(response.status_code, 422)
