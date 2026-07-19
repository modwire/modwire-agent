from dataclasses import dataclass
from uuid import UUID, uuid4

from ...domain.artifact.artifact_policy import ArtifactPolicy
from ...domain.operation.operation_context import OperationContext
from ...domain.operation.operation_execution import OperationExecution
from ...domain.operation.operation_policy import OperationPolicy
from ...domain.run.invalid_stage_submission import InvalidStageSubmission
from ...domain.run.plan_run_status import PlanRunStatus
from ...ports.artifact.plan_artifact_store import PlanArtifactStore
from ...ports.contracts.schema_validator import SchemaValidator
from ...ports.definition.plan_definition_store import PlanDefinitionStore
from ...ports.operation.operation_catalog import OperationCatalog
from ...ports.operation.operation_execution_store import OperationExecutionStore
from ...ports.run.plan_run_store import PlanRunStore


@dataclass(frozen=True, slots=True)
class ExecuteStageOperation:
    definitions: PlanDefinitionStore
    runs: PlanRunStore
    executions: OperationExecutionStore
    artifacts: PlanArtifactStore
    operations: OperationCatalog
    schemas: SchemaValidator
    policy: OperationPolicy
    artifact_policy: ArtifactPolicy

    def execute(self, run_id: UUID, operation_id: str) -> None:
        run = self.runs.get(run_id)
        if run.status != PlanRunStatus.ACTIVE:
            raise InvalidStageSubmission("A completed run does not execute operations.")
        definition = self.definitions.get(run.definition_id)
        operation = self.policy.get(definition, operation_id)
        if operation.stage_id != run.current_stage_id:
            raise InvalidStageSubmission("An operation may only run in its current stage.")
        self.schemas.require_valid_value(operation.input_schema, run.current_input)
        claim = self.policy.claim(run.identifier, operation.identifier)
        if not self.executions.try_claim(claim):
            if self.executions.is_complete(run.identifier, operation.identifier):
                return
            raise InvalidStageSubmission("The operation is already running.")
        try:
            artifacts = {artifact_id: self.artifacts.get(run.identifier, artifact_id).payload for artifact_id in operation.required_artifact_ids}
            context = OperationContext(run.identifier, operation.identifier, run.current_input, artifacts, operation.configuration)
            output = self.operations.resolve(operation.extension_key, operation.extension_version).execute(context)
            self.schemas.require_valid_value(operation.output_schema, output)
            artifact = self._produce_artifact(definition, operation.produced_artifact_id, run.identifier, output)
            self.executions.complete(self.policy.complete(claim, output), artifact)
        except Exception:
            self.executions.release(claim)
            raise

    def _produce_artifact(self, definition, artifact_id: str, run_id: UUID, output: dict):
        if not artifact_id:
            return None
        artifact = next(item for item in definition.artifacts if item.identifier == artifact_id)
        self.schemas.require_valid_value(artifact.schema, output)
        return self.artifact_policy.produce(run_id, artifact.identifier, output)
