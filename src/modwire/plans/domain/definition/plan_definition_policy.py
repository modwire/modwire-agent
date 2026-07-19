from dataclasses import dataclass
from uuid import uuid4

from ..artifact.artifact_definition import ArtifactDefinition
from ..gate.gate_definition import GateDefinition
from ..operation.operation_definition import OperationDefinition
from .artifact_definition_policy import ArtifactDefinitionPolicy
from .plan_definition import PlanDefinition
from .stage_definition import StageDefinition
from .transition_definition import TransitionDefinition


@dataclass(frozen=True, slots=True)
class PlanDefinitionPolicy:
    artifacts: ArtifactDefinitionPolicy

    def publish(self, name: str, version: int, start_stage_id: str, stages: list[StageDefinition], transitions: list[TransitionDefinition], gates: list[GateDefinition], operations: list[OperationDefinition], artifacts: list[ArtifactDefinition]) -> PlanDefinition:
        self.artifacts.require_valid_declarations(tuple(operations), tuple(artifacts))
        return PlanDefinition(uuid4(), name, version, start_stage_id, tuple(stages), tuple(transitions), tuple(gates), tuple(operations), tuple(artifacts))
