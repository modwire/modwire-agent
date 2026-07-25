from dataclasses import dataclass

from ...domain.artifact.artifact_definition import ArtifactDefinition
from ...domain.definition.plan_definition import PlanDefinition
from ...domain.definition.plan_definition_policy import PlanDefinitionPolicy
from ...domain.definition.stage_definition import StageDefinition
from ...domain.definition.transition_definition import TransitionDefinition
from ...domain.gate.gate_definition import GateDefinition
from ...domain.operation.operation_definition import OperationDefinition
from ...ports.contracts.schema_validator import SchemaValidator
from ...ports.definition.plan_definition_store import PlanDefinitionStore
from ...ports.operation.operation_catalog import OperationCatalog


@dataclass(frozen=True, slots=True)
class PublishPlanDefinition:
    definitions: PlanDefinitionStore
    schemas: SchemaValidator
    policy: PlanDefinitionPolicy
    operations: OperationCatalog

    def execute(
        self,
        name: str,
        start_stage_id: str,
        stages: list[StageDefinition],
        transitions: list[TransitionDefinition],
        gates: list[GateDefinition],
        operations: list[OperationDefinition],
        artifacts: list[ArtifactDefinition],
    ) -> PlanDefinition:
        for stage in stages:
            self.schemas.require_valid_schema(stage.input_schema)
            self.schemas.require_valid_schema(stage.submission_schema)
        for gate in gates:
            self.schemas.require_valid_schema(gate.evidence_schema)
        for operation in operations:
            self._validate_operation(operation)
        for artifact in artifacts:
            self.schemas.require_valid_schema(artifact.schema)
        definition = self.policy.publish(
            name, self.definitions.next_version(name), start_stage_id, stages, transitions, gates, operations, artifacts
        )
        self._require_compatible_stage_contracts(definition)
        self._require_compatible_artifact_contracts(definition)
        self.definitions.publish(definition)
        return definition

    def _validate_operation(self, operation: OperationDefinition) -> None:
        self.schemas.require_valid_schema(operation.input_schema)
        self.schemas.require_valid_schema(operation.output_schema)
        self.operations.resolve(operation.extension_key, operation.extension_version).require_valid_configuration(
            operation.configuration
        )

    def _require_compatible_stage_contracts(self, definition: PlanDefinition) -> None:
        for transition in definition.transitions:
            source = definition.stage(transition.source_stage_id)
            target = definition.stage(transition.target_stage_id)
            self.schemas.require_compatible_values(source.submission_schema, target.input_schema)

    def _require_compatible_artifact_contracts(self, definition: PlanDefinition) -> None:
        artifacts = {artifact.identifier: artifact for artifact in definition.artifacts}
        for operation in definition.operations:
            if operation.produced_artifact_id:
                self.schemas.require_compatible_values(
                    operation.output_schema, artifacts[operation.produced_artifact_id].schema
                )
