from uuid import UUID

from modwire_hex.django import DjangoRepository

from ...domain.run.plan_run import PlanRun
from ...domain.run.plan_run_status import PlanRunStatus
from ...ports.run.plan_run_store import PlanRunStore
from ..django.models import PlanRunModel


class DjangoPlanRunStore(DjangoRepository[PlanRun, PlanRunModel, UUID], PlanRunStore):
    def key_of(self, domain: PlanRun) -> UUID:
        return domain.identifier

    def find_record(self, key: UUID) -> PlanRunModel | None:
        try:
            return PlanRunModel.objects.get(identifier=key)
        except PlanRunModel.DoesNotExist:
            return None

    def create_record(self, domain: PlanRun) -> PlanRunModel:
        return PlanRunModel(
            identifier=domain.identifier,
            definition_id=domain.definition_id,
            definition_version=domain.definition_version,
            current_stage_id=domain.current_stage_id,
            current_input=domain.current_input,
            status=domain.status,
            revision=domain.revision,
        )

    def update_record(self, model: PlanRunModel, domain: PlanRun) -> None:
        model.definition_version = domain.definition_version
        model.current_stage_id = domain.current_stage_id
        model.current_input = domain.current_input
        model.status = domain.status
        model.revision = domain.revision

    def to_domain(self, model: PlanRunModel) -> PlanRun:
        return PlanRun(
            model.identifier,
            model.definition_id,
            model.definition_version,
            model.current_stage_id,
            model.current_input,
            PlanRunStatus(model.status),
            model.revision,
        )

    def get(self, run_id: UUID) -> PlanRun:
        run = self.load(run_id)
        if run is None:
            raise LookupError(f"Plan run {run_id!r} was not found.")
        return run
