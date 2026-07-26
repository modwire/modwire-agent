from uuid import UUID

from django.db import IntegrityError, transaction

from ...domain.gate.gate_satisfaction import GateSatisfaction
from ...domain.run.invalid_stage_submission import InvalidStageSubmission
from ...ports.outbound import GateSatisfactionStore
from ..django.models import GateSatisfactionModel


class DjangoGateSatisfactionStore(GateSatisfactionStore):
    def find(self, run_id: UUID, gate_id: str) -> GateSatisfaction | None:
        model = GateSatisfactionModel.objects.filter(
            satisfaction_key=self._satisfaction_key_for(run_id, gate_id)
        ).first()
        if model is None:
            return None
        return GateSatisfaction(model.identifier, model.plan_run_id, model.gate_id, model.evidence)

    def satisfied_gate_ids(self, run_id: UUID) -> set[str]:
        return set(GateSatisfactionModel.objects.filter(plan_run_id=run_id).values_list("gate_id", flat=True))

    def save(self, satisfaction: GateSatisfaction) -> None:
        key = self._satisfaction_key(satisfaction)
        existing = GateSatisfactionModel.objects.filter(satisfaction_key=key).first()
        if existing is not None:
            self._require_same_evidence(existing, satisfaction)
            return
        try:
            with transaction.atomic():
                GateSatisfactionModel.objects.create(
                    identifier=satisfaction.identifier,
                    plan_run_id=satisfaction.plan_run_id,
                    gate_id=satisfaction.gate_id,
                    satisfaction_key=key,
                    evidence=satisfaction.evidence,
                )
        except IntegrityError:
            existing = GateSatisfactionModel.objects.get(satisfaction_key=key)
            self._require_same_evidence(existing, satisfaction)

    def _require_same_evidence(self, existing: GateSatisfactionModel, satisfaction: GateSatisfaction) -> None:
        if existing.evidence != satisfaction.evidence:
            raise InvalidStageSubmission("A gate is already satisfied with different evidence.")

    def _satisfaction_key(self, satisfaction: GateSatisfaction) -> str:
        return self._satisfaction_key_for(satisfaction.plan_run_id, satisfaction.gate_id)

    def _satisfaction_key_for(self, run_id: UUID, gate_id: str) -> str:
        return f"{run_id}:{gate_id}"
