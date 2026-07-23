from .artifact_definition_input import ArtifactDefinitionInput
from .gate_definition_input import GateDefinitionInput
from .operation_definition_input import OperationDefinitionInput
from .stage_definition_input import StageDefinitionInput
from .strict import StrictSchema
from .transition_definition_input import TransitionDefinitionInput


class PlanDefinitionInput(StrictSchema):
    name: str
    start_stage_id: str
    stages: list[StageDefinitionInput]
    transitions: list[TransitionDefinitionInput]
    gates: list[GateDefinitionInput]
    operations: list[OperationDefinitionInput]
    artifacts: list[ArtifactDefinitionInput] = []
