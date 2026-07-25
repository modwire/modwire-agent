from typing import Any
from uuid import UUID, uuid4

from ..definition.invalid_plan_definition import InvalidPlanDefinition
from ..definition.plan_definition import PlanDefinition
from ..run.invalid_stage_submission import InvalidStageSubmission
from .gate_satisfaction import GateSatisfaction


class GatePolicy:
    def get(self, definition: PlanDefinition, gate_id: str):
        for gate in definition.gates:
            if gate.identifier == gate_id:
                return gate
        raise InvalidPlanDefinition(f"Unknown gate: {gate_id!r}.")

    def ids_for(self, definition: PlanDefinition, stage_id: str) -> set[str]:
        return {gate.identifier for gate in definition.gates if gate.stage_id == stage_id}

    def satisfy(self, run_id: UUID, gate_id: str, evidence: dict[str, Any]) -> GateSatisfaction:
        return GateSatisfaction(uuid4(), run_id, gate_id, evidence)

    def allow_retry(self, satisfaction: GateSatisfaction, evidence: dict[str, Any]) -> None:
        if satisfaction.evidence != evidence:
            raise InvalidStageSubmission("A gate is already satisfied with different evidence.")
