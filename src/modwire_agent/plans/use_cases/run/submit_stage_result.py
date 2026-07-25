from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ...domain.gate.gate_policy import GatePolicy
from ...domain.operation.operation_policy import OperationPolicy
from ...domain.run.invalid_stage_submission import InvalidStageSubmission
from ...domain.run.plan_run_policy import PlanRunPolicy
from ...domain.run.plan_run_status import PlanRunStatus
from ...ports.contracts.schema_validator import SchemaValidator
from ...ports.definition.plan_definition_store import PlanDefinitionStore
from ...ports.gate.gate_satisfaction_store import GateSatisfactionStore
from ...ports.operation.operation_execution_store import OperationExecutionStore
from ...ports.run.plan_run_store import PlanRunStore
from ...ports.run.stage_transition_store import StageTransitionStore


@dataclass(frozen=True, slots=True)
class SubmitStageResult:
    definitions: PlanDefinitionStore
    runs: PlanRunStore
    transitions: StageTransitionStore
    gates: GateSatisfactionStore
    executions: OperationExecutionStore
    schemas: SchemaValidator
    policy: PlanRunPolicy
    gate_policy: GatePolicy
    operation_policy: OperationPolicy

    def execute(self, run_id: UUID, payload: dict[str, Any]):
        run = self.runs.get(run_id)
        if run.status != PlanRunStatus.ACTIVE:
            raise InvalidStageSubmission("A completed run does not accept submissions.")
        definition = self.definitions.get(run.definition_id)
        stage = definition.stage(run.current_stage_id)
        self._require_completed_operations(run.identifier, stage.identifier, definition)
        self._require_satisfied_gates(run.identifier, stage.identifier, definition)
        self.schemas.require_valid_value(stage.submission_schema, payload)
        next_stage_id = definition.next_stage_id(stage.identifier)
        self._require_valid_next_stage_input(definition, next_stage_id, payload)
        transition = self.policy.transition(run, next_stage_id, payload)
        self.transitions.commit(transition)
        updated = transition.updated_run
        return updated

    def _require_satisfied_gates(self, run_id: UUID, stage_id: str, definition) -> None:
        required = self.gate_policy.ids_for(definition, stage_id)
        satisfied = self.gates.satisfied_gate_ids(run_id)
        missing = required - satisfied
        if missing:
            raise InvalidStageSubmission(f"Unsatisfied gates: {', '.join(sorted(missing))}.")

    def _require_completed_operations(self, run_id: UUID, stage_id: str, definition) -> None:
        required = self.operation_policy.ids_for(definition, stage_id)
        completed = self.executions.completed_operation_ids(run_id)
        missing = required - completed
        if missing:
            raise InvalidStageSubmission(f"Incomplete operations: {', '.join(sorted(missing))}.")

    def _require_valid_next_stage_input(self, definition, next_stage_id: str, payload: dict[str, Any]) -> None:
        if not next_stage_id:
            return
        next_stage = definition.stage(next_stage_id)
        self.schemas.require_valid_value(next_stage.input_schema, payload)
