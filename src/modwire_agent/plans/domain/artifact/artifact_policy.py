from typing import Any
from uuid import UUID, uuid4

from .plan_artifact import PlanArtifact


class ArtifactPolicy:
    def produce(self, run_id: UUID, artifact_id: str, payload: dict[str, Any]) -> PlanArtifact:
        return PlanArtifact(uuid4(), run_id, artifact_id, payload)
