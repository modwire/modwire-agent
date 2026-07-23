from typing import Any

from modwire_hex.django import DjangoRequest
from ninja_extra import ControllerBase, api_controller, route

from ...domain.artifact.artifact_definition import ArtifactDefinition
from ...domain.definition.stage_definition import StageDefinition
from ...domain.definition.transition_definition import TransitionDefinition
from ...domain.gate.gate_definition import GateDefinition
from ...domain.operation.operation_definition import OperationDefinition
from ...use_cases.definition.publish_plan_definition import PublishPlanDefinition
from .schemas.plan_definition_input import PlanDefinitionInput
from .schemas.plan_definition_output import PlanDefinitionOutput


@api_controller("/plans/definitions", tags=["plans"])
class PublishDefinitionController(ControllerBase):
    @route.post("", response={201: PlanDefinitionOutput}, operation_id="publish_plan_definition")
    def publish(self, request: Any, payload: PlanDefinitionInput) -> tuple[int, PlanDefinitionOutput]:
        stages = [StageDefinition(stage.id, stage.input_schema, stage.submission_schema) for stage in payload.stages]
        transitions = [TransitionDefinition(item.source_stage_id, item.target_stage_id) for item in payload.transitions]
        gates = [GateDefinition(item.id, item.stage_id, item.evidence_schema) for item in payload.gates]
        operations = [OperationDefinition(item.id, item.stage_id, item.extension_key, item.extension_version, item.configuration, item.input_schema, item.output_schema, item.produced_artifact_id, tuple(item.required_artifact_ids)) for item in payload.operations]
        artifacts = [ArtifactDefinition(item.id, item.producer_operation_id, item.output_schema) for item in payload.artifacts]
        definition = DjangoRequest.resolve(request, PublishPlanDefinition).execute(payload.name, payload.start_stage_id, stages, transitions, gates, operations, artifacts)
        return 201, PlanDefinitionOutput(id=str(definition.identifier), version=definition.version, start_stage_id=definition.start_stage_id)
