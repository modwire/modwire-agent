from abc import ABC, abstractmethod
from uuid import UUID

from ...domain.artifact.plan_artifact import PlanArtifact


class PlanArtifactStore(ABC):
    @abstractmethod
    def get(self, run_id: UUID, artifact_id: str) -> PlanArtifact:
        raise NotImplementedError
