from dataclasses import asdict
from uuid import UUID

from django.db.models import Max

from ...domain.artifact.artifact_definition import ArtifactDefinition
from ...domain.definition.plan_definition import PlanDefinition
from ...domain.definition.stage_definition import StageDefinition
from ...domain.definition.transition_definition import TransitionDefinition
from ...domain.gate.gate_definition import GateDefinition
from ...domain.operation.operation_definition import OperationDefinition
from ...ports.outbound import PlanDefinitionStore
from ..django.models import PlanDefinitionModel


class DjangoPlanDefinitionStore(PlanDefinitionStore):
    def next_version(self, name: str) -> int:
        latest = PlanDefinitionModel.objects.filter(name=name).aggregate(version=Max("version"))["version"]
        return (latest or 0) + 1

    def publish(self, definition: PlanDefinition) -> None:
        PlanDefinitionModel.objects.create(
            identifier=definition.identifier,
            name=definition.name,
            version=definition.version,
            publication_key=self._publication_key(definition.name, definition.version),
            start_stage_id=definition.start_stage_id,
            stages=self._stages(definition),
            transitions=self._transitions(definition),
            gates=self._gates(definition),
            operations=self._operations(definition),
            artifacts=self._artifacts(definition),
        )

    def to_domain(self, model: PlanDefinitionModel) -> PlanDefinition:
        stages = tuple(
            StageDefinition(item["identifier"], item["input_schema"], item["submission_schema"])
            for item in model.stages
        )
        transitions = tuple(
            TransitionDefinition(item["source_stage_id"], item["target_stage_id"]) for item in model.transitions
        )
        gates = tuple(
            GateDefinition(item["identifier"], item["stage_id"], item["evidence_schema"]) for item in model.gates
        )
        operations = tuple(
            OperationDefinition(
                item["identifier"],
                item["stage_id"],
                item["extension_key"],
                item["extension_version"],
                item["configuration"],
                item["input_schema"],
                item["output_schema"],
                item["produced_artifact_id"],
                tuple(item["required_artifact_ids"]),
            )
            for item in model.operations
        )
        artifacts = tuple(
            ArtifactDefinition(item["identifier"], item["producer_operation_id"], item["schema"])
            for item in model.artifacts
        )
        return PlanDefinition(
            model.identifier,
            model.name,
            model.version,
            model.start_stage_id,
            stages,
            transitions,
            gates,
            operations,
            artifacts,
        )

    def get(self, definition_id: UUID) -> PlanDefinition:
        try:
            model = PlanDefinitionModel.objects.get(identifier=definition_id)
        except PlanDefinitionModel.DoesNotExist:
            raise LookupError(f"Plan definition {definition_id!r} was not found.") from None
        return self.to_domain(model)

    def _stages(self, domain: PlanDefinition) -> list[dict]:
        return [asdict(stage) for stage in domain.stages]

    def _transitions(self, domain: PlanDefinition) -> list[dict]:
        return [asdict(transition) for transition in domain.transitions]

    def _gates(self, domain: PlanDefinition) -> list[dict]:
        return [asdict(gate) for gate in domain.gates]

    def _operations(self, domain: PlanDefinition) -> list[dict]:
        return [asdict(operation) for operation in domain.operations]

    def _artifacts(self, domain: PlanDefinition) -> list[dict]:
        return [asdict(artifact) for artifact in domain.artifacts]

    def _publication_key(self, name: str, version: int) -> str:
        return f"{name}:{version}"
