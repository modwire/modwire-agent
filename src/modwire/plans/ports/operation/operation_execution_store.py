from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.operation.operation_execution import OperationExecution
from ...domain.operation.operation_claim import OperationClaim
from ...domain.artifact.plan_artifact import PlanArtifact


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
