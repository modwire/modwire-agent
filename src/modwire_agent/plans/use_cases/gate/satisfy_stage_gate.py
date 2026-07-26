from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ...domain.gate.gate_policy import GatePolicy
from ...domain.run.invalid_stage_submission import InvalidStageSubmission
from ...domain.run.plan_run_status import PlanRunStatus
from ...ports.outbound import GateSatisfactionStore, PlanDefinitionStore, PlanRunStore, SchemaValidator


@dataclass(frozen=True, slots=True)
class SatisfyStageGate:
    definitions: PlanDefinitionStore
    runs: PlanRunStore
    gates: GateSatisfactionStore
    schemas: SchemaValidator
    policy: GatePolicy

    def execute(self, run_id: UUID, gate_id: str, evidence: dict[str, Any]) -> None:
        run = self.runs.get(run_id)
        if run.status != PlanRunStatus.ACTIVE:
            raise InvalidStageSubmission("A completed run does not accept gate evidence.")
        definition = self.definitions.get(run.definition_id)
        gate = self.policy.get(definition, gate_id)
        if gate.stage_id != run.current_stage_id:
            raise InvalidStageSubmission("A gate may only be satisfied in its current stage.")
        self.schemas.require_valid_value(gate.evidence_schema, evidence)
        existing = self.gates.find(run.identifier, gate.identifier)
        if existing is not None:
            self.policy.allow_retry(existing, evidence)
            return
        self.gates.save(self.policy.satisfy(run.identifier, gate.identifier, evidence))
