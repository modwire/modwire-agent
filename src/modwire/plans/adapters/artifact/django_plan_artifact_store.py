from uuid import UUID

from ...domain.artifact.plan_artifact import PlanArtifact
from ...ports.artifact.plan_artifact_store import PlanArtifactStore
from ..django.models import PlanArtifactModel


class DjangoPlanArtifactStore(PlanArtifactStore):
    def get(self, run_id: UUID, artifact_id: str) -> PlanArtifact:
        try:
            model = PlanArtifactModel.objects.get(artifact_key=self._artifact_key(run_id, artifact_id))
        except PlanArtifactModel.DoesNotExist:
            raise LookupError(f"Artifact {artifact_id!r} was not produced for plan run {run_id!r}.")
        return PlanArtifact(model.identifier, model.plan_run_id, model.artifact_id, model.payload)

    def _artifact_key(self, run_id: UUID, artifact_id: str) -> str:
        return f"{run_id}:{artifact_id}"
