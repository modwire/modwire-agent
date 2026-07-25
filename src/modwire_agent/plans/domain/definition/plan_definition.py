from dataclasses import dataclass
from uuid import UUID

from ..artifact.artifact_definition import ArtifactDefinition
from ..gate.gate_definition import GateDefinition
from ..operation.operation_definition import OperationDefinition
from .invalid_plan_definition import InvalidPlanDefinition
from .stage_definition import StageDefinition
from .transition_definition import TransitionDefinition


@dataclass(frozen=True, slots=True)
class PlanDefinition:
    identifier: UUID
    name: str
    version: int
    start_stage_id: str
    stages: tuple[StageDefinition, ...]
    transitions: tuple[TransitionDefinition, ...]
    gates: tuple[GateDefinition, ...]
    operations: tuple[OperationDefinition, ...]
    artifacts: tuple[ArtifactDefinition, ...]

    def __post_init__(self) -> None:
        self._require_valid_name()
        self._require_valid_stage_ids()
        self._require_valid_transitions()
        self._require_valid_gates()
        self._require_valid_operations()
        self._require_all_stages_reachable()
        self._require_terminal_path()

    def stage(self, stage_id: str) -> StageDefinition:
        for stage in self.stages:
            if stage.identifier == stage_id:
                return stage
        raise InvalidPlanDefinition(f"Unknown stage: {stage_id!r}.")

    def next_stage_id(self, stage_id: str) -> str:
        matches = [
            transition.target_stage_id for transition in self.transitions if transition.source_stage_id == stage_id
        ]
        if len(matches) > 1:
            raise InvalidPlanDefinition(f"Stage {stage_id!r} has multiple transitions.")
        return matches[0] if matches else ""

    def _require_valid_name(self) -> None:
        if not self.name.strip() or self.version < 1:
            raise InvalidPlanDefinition("A definition needs a name and positive version.")

    def _require_valid_stage_ids(self) -> None:
        stage_ids = [stage.identifier for stage in self.stages]
        if not stage_ids or not all(stage_ids) or len(stage_ids) != len(set(stage_ids)):
            raise InvalidPlanDefinition("A definition needs uniquely named stages.")
        if self.start_stage_id not in stage_ids:
            raise InvalidPlanDefinition("The start stage must be declared.")

    def _require_valid_transitions(self) -> None:
        stage_ids = {stage.identifier for stage in self.stages}
        source_ids = [transition.source_stage_id for transition in self.transitions]
        if any(identifier not in stage_ids for identifier in source_ids):
            raise InvalidPlanDefinition("A transition source must be declared.")
        target_ids = [transition.target_stage_id for transition in self.transitions]
        if any(identifier not in stage_ids for identifier in target_ids):
            raise InvalidPlanDefinition("A transition target must be declared.")
        if len(source_ids) != len(set(source_ids)):
            raise InvalidPlanDefinition("A stage may have at most one transition.")
        if self.start_stage_id in target_ids:
            raise InvalidPlanDefinition("The start stage may not have an incoming transition.")

    def _require_valid_gates(self) -> None:
        stage_ids = {stage.identifier for stage in self.stages}
        gate_ids = [gate.identifier for gate in self.gates]
        if not all(gate_ids) or len(gate_ids) != len(set(gate_ids)):
            raise InvalidPlanDefinition("A definition needs uniquely named gates.")
        if any(gate.stage_id not in stage_ids for gate in self.gates):
            raise InvalidPlanDefinition("A gate must belong to a declared stage.")

    def _require_valid_operations(self) -> None:
        stage_ids = {stage.identifier for stage in self.stages}
        operation_ids = [operation.identifier for operation in self.operations]
        if not all(operation_ids) or len(operation_ids) != len(set(operation_ids)):
            raise InvalidPlanDefinition("A definition needs uniquely named operations.")
        if any(operation.stage_id not in stage_ids for operation in self.operations):
            raise InvalidPlanDefinition("An operation must belong to a declared stage.")

    def _require_all_stages_reachable(self) -> None:
        reachable = {self.start_stage_id}
        while True:
            targets = {
                transition.target_stage_id for transition in self.transitions if transition.source_stage_id in reachable
            }
            expanded = reachable | targets
            if expanded == reachable:
                break
            reachable = expanded
        if reachable != {stage.identifier for stage in self.stages}:
            raise InvalidPlanDefinition("Every stage must be reachable from the start stage.")

    def _require_terminal_path(self) -> None:
        visited: set[str] = set()
        stage_id = self.start_stage_id
        while stage_id:
            if stage_id in visited:
                raise InvalidPlanDefinition("A definition needs a terminal path, not a cycle.")
            visited.add(stage_id)
            stage_id = self.next_stage_id(stage_id)
