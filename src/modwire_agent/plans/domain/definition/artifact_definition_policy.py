from ..artifact.artifact_definition import ArtifactDefinition
from ..operation.operation_definition import OperationDefinition
from .invalid_plan_definition import InvalidPlanDefinition


class ArtifactDefinitionPolicy:
    def require_valid_declarations(
        self, operations: tuple[OperationDefinition, ...], artifacts: tuple[ArtifactDefinition, ...]
    ) -> None:
        artifact_ids = [artifact.identifier for artifact in artifacts]
        operation_ids = {operation.identifier for operation in operations}
        if not all(artifact_ids) or len(artifact_ids) != len(set(artifact_ids)):
            raise InvalidPlanDefinition("A definition needs uniquely named artifacts.")
        if any(artifact.producer_operation_id not in operation_ids for artifact in artifacts):
            raise InvalidPlanDefinition("An artifact must name a declared producer operation.")
        declared = {artifact.identifier: artifact for artifact in artifacts}
        for operation in operations:
            if operation.produced_artifact_id:
                artifact = declared.get(operation.produced_artifact_id)
                if artifact is None or artifact.producer_operation_id != operation.identifier:
                    raise InvalidPlanDefinition("An operation may only produce its declared artifact.")
            if len(operation.required_artifact_ids) != len(set(operation.required_artifact_ids)):
                raise InvalidPlanDefinition("An operation may require an artifact at most once.")
            if any(identifier not in declared for identifier in operation.required_artifact_ids):
                raise InvalidPlanDefinition("An operation may only require declared artifacts.")
            if operation.produced_artifact_id and operation.produced_artifact_id in operation.required_artifact_ids:
                raise InvalidPlanDefinition("An operation may not require its own output artifact.")
