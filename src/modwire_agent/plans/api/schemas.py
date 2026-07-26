from typing import Any

from ninja import Schema
from pydantic import ConfigDict


class StrictSchema(Schema):
    model_config = ConfigDict(extra="forbid")


class ArtifactDefinitionInput(Schema):
    id: str
    producer_operation_id: str
    output_schema: dict[str, Any]


class GateDefinitionInput(Schema):
    id: str
    stage_id: str
    evidence_schema: dict[str, Any]


class GateSatisfactionInput(Schema):
    evidence: dict[str, Any]


class OperationDefinitionInput(Schema):
    id: str
    stage_id: str
    extension_key: str
    extension_version: int
    configuration: dict[str, Any]
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    produced_artifact_id: str
    required_artifact_ids: list[str] = []


class StageDefinitionInput(Schema):
    id: str
    input_schema: dict[str, Any]
    submission_schema: dict[str, Any]


class StageSubmissionInput(Schema):
    payload: dict[str, Any]


class TransitionDefinitionInput(Schema):
    source_stage_id: str
    target_stage_id: str


class PlanDefinitionInput(StrictSchema):
    name: str
    start_stage_id: str
    stages: list[StageDefinitionInput]
    transitions: list[TransitionDefinitionInput]
    gates: list[GateDefinitionInput]
    operations: list[OperationDefinitionInput]
    artifacts: list[ArtifactDefinitionInput] = []


class PlanDefinitionOutput(Schema):
    id: str
    version: int
    start_stage_id: str


class PlanRunInput(Schema):
    definition_id: str
    initial_input: dict[str, Any]


class PlanRunOutput(Schema):
    id: str
    current_stage_id: str
    status: str
