from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

from ..domain.artifact.plan_artifact import PlanArtifact
from ..domain.definition.plan_definition import PlanDefinition
from ..domain.gate.gate_satisfaction import GateSatisfaction
from ..domain.operation.operation_claim import OperationClaim
from ..domain.operation.operation_context import OperationContext
from ..domain.operation.operation_execution import OperationExecution
from ..domain.run.plan_run import PlanRun
from ..domain.run.stage_transition import StageTransition


class PlanArtifactStore(ABC):
    @abstractmethod
    def get(self, run_id: UUID, artifact_id: str) -> PlanArtifact:
        raise NotImplementedError


class SchemaValidator(ABC):
    @abstractmethod
    def require_valid_schema(self, schema: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def require_valid_value(self, schema: dict[str, Any], value: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def require_compatible_values(self, output_schema: dict[str, Any], input_schema: dict[str, Any]) -> None:
        raise NotImplementedError


class PlanDefinitionStore(ABC):
    @abstractmethod
    def get(self, definition_id: UUID) -> PlanDefinition:
        raise NotImplementedError

    @abstractmethod
    def next_version(self, name: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def publish(self, definition: PlanDefinition) -> None:
        raise NotImplementedError


class GateSatisfactionStore(ABC):
    @abstractmethod
    def find(self, run_id: UUID, gate_id: str) -> GateSatisfaction | None:
        raise NotImplementedError

    @abstractmethod
    def satisfied_gate_ids(self, run_id: UUID) -> set[str]:
        raise NotImplementedError

    @abstractmethod
    def save(self, satisfaction: GateSatisfaction) -> None:
        raise NotImplementedError


class OperationHandler(ABC):
    @abstractmethod
    def key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def version(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def require_valid_configuration(self, configuration: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(self, context: OperationContext) -> dict:
        raise NotImplementedError


class OperationCatalog(ABC):
    @abstractmethod
    def resolve(self, extension_key: str, extension_version: int) -> OperationHandler:
        raise NotImplementedError


class OperationExecutionStore(ABC):
    @abstractmethod
    def completed_operation_ids(self, run_id: UUID) -> set[str]:
        raise NotImplementedError

    @abstractmethod
    def try_claim(self, claim: OperationClaim) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_complete(self, run_id: UUID, operation_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def complete(self, execution: OperationExecution, artifact: PlanArtifact | None) -> None:
        raise NotImplementedError

    @abstractmethod
    def release(self, claim: OperationClaim) -> None:
        raise NotImplementedError


class PlanRunStore(ABC):
    @abstractmethod
    def get(self, run_id: UUID) -> PlanRun:
        raise NotImplementedError

    @abstractmethod
    def save(self, run: PlanRun) -> None:
        raise NotImplementedError


class StageTransitionStore(ABC):
    @abstractmethod
    def commit(self, transition: StageTransition) -> None:
        raise NotImplementedError
