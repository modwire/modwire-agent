from django.db import transaction

from ...domain.run.invalid_stage_submission import InvalidStageSubmission
from ...domain.run.stage_transition import StageTransition
from ...ports.outbound import StageTransitionStore
from ..django.models import PlanRunModel, StageSubmissionModel


class DjangoStageTransitionStore(StageTransitionStore):
    def commit(self, transition: StageTransition) -> None:
        with transaction.atomic():
            updated = PlanRunModel.objects.filter(
                identifier=transition.updated_run.identifier, revision=transition.expected_revision
            ).update(
                current_stage_id=transition.updated_run.current_stage_id,
                current_input=transition.updated_run.current_input,
                status=transition.updated_run.status,
                revision=transition.updated_run.revision,
            )
            if updated != 1:
                raise InvalidStageSubmission(
                    "The plan run changed while its stage was being submitted. Retry with its current state."
                )
            StageSubmissionModel.objects.create(
                identifier=transition.submission.identifier,
                plan_run_id=transition.submission.plan_run_id,
                stage_id=transition.submission.stage_id,
                payload=transition.submission.payload,
            )
