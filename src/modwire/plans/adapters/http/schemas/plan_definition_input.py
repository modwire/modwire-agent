from ninja import Schema

from .stage_definition_input import StageDefinitionInput
from .transition_definition_input import TransitionDefinitionInput
from .gate_definition_input import GateDefinitionInput
from .operation_definition_input import OperationDefinitionInput
from .artifact_definition_input import ArtifactDefinitionInput


class PlanDefinitionInput(Schema):
    name: str
    start_stage_id: str
    stages: list[StageDefinitionInput]
    transitions: list[TransitionDefinitionInput]
    gates: list[GateDefinitionInput]
    operations: list[OperationDefinitionInput]
    artifacts: list[ArtifactDefinitionInput] = []
