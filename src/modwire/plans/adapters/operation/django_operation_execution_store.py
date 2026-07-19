from uuid import UUID

from django.db import IntegrityError, transaction

from ...domain.artifact.plan_artifact import PlanArtifact
from ...domain.operation.operation_claim import OperationClaim
from ...domain.operation.operation_execution import OperationExecution
from ...domain.run.invalid_stage_submission import InvalidStageSubmission
from ...ports.operation.operation_execution_store import OperationExecutionStore
from ..django.models import OperationExecutionModel, PlanArtifactModel


class DjangoOperationExecutionStore(OperationExecutionStore):
    def completed_operation_ids(self, run_id: UUID) -> set[str]:
        return set(OperationExecutionModel.objects.filter(plan_run_id=run_id, status="complete").values_list("operation_id", flat=True))

    def try_claim(self, claim: OperationClaim) -> bool:
        try:
            OperationExecutionModel.objects.create(identifier=claim.identifier, plan_run_id=claim.plan_run_id, operation_id=claim.operation_id, execution_key=f"{claim.plan_run_id}:{claim.operation_id}", status="pending", output={})
        except IntegrityError:
            return False
        return True

    def is_complete(self, run_id: UUID, operation_id: str) -> bool:
        return OperationExecutionModel.objects.filter(execution_key=f"{run_id}:{operation_id}", status="complete").exists()

    def complete(self, execution: OperationExecution, artifact: PlanArtifact | None) -> None:
        try:
            with transaction.atomic():
                updated = OperationExecutionModel.objects.filter(identifier=execution.identifier, status="pending").update(status="complete", output=execution.output)
                if updated != 1:
                    raise InvalidStageSubmission("The operation claim is no longer active.")
                if artifact is not None:
                    PlanArtifactModel.objects.create(identifier=artifact.identifier, plan_run_id=artifact.plan_run_id, artifact_id=artifact.artifact_id, artifact_key=f"{artifact.plan_run_id}:{artifact.artifact_id}", payload=artifact.payload)
        except IntegrityError:
            self._require_same_result(execution, artifact)

    def _require_same_result(self, execution: OperationExecution, artifact: PlanArtifact | None) -> None:
        existing = OperationExecutionModel.objects.get(execution_key=self._execution_key(execution))
        if existing.output != execution.output:
            raise InvalidStageSubmission("An operation is already complete with different output.")
        if artifact is not None:
            existing_artifact = PlanArtifactModel.objects.get(artifact_key=f"{artifact.plan_run_id}:{artifact.artifact_id}")
            if existing_artifact.payload != artifact.payload:
                raise InvalidStageSubmission("An artifact is already produced with different payload.")

    def _execution_key(self, execution: OperationExecution) -> str:
        return f"{execution.plan_run_id}:{execution.operation_id}"

    def release(self, claim: OperationClaim) -> None:
        OperationExecutionModel.objects.filter(identifier=claim.identifier, status="pending").delete()
