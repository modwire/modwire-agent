from dataclasses import dataclass

from django.db import transaction
from django.shortcuts import get_object_or_404
from wireup import injectable

from modwire.apps.languages.models.language import Language

from ...models.scaffolding import Scaffolding
from .contracts import ConvergencePlan, ConvergenceResult, TemplateSpec, VariableSpec
from .planner import ScaffoldingConvergencePlanner
from .validator import ScaffoldingAggregateValidator
from .writer import ScaffoldingAggregateWriter


@injectable
@dataclass(frozen=True)
class ScaffoldingConvergenceService:
    validator: ScaffoldingAggregateValidator
    planner: ScaffoldingConvergencePlanner
    writer: ScaffoldingAggregateWriter

    def converge(
        self,
        *,
        language_id: str,
        name: str,
        description: str,
        variables: list[VariableSpec],
        templates: list[TemplateSpec],
        dry_run: bool,
    ) -> ConvergenceResult:
        language = get_object_or_404(Language, id=language_id)
        current = self._current(language, name)
        desired = self.validator.validate(language, current, name, description, variables, templates)
        plan = self.planner.plan(current, desired)
        if dry_run:
            return self._result(name, True, plan)

        with transaction.atomic():
            current = self._current(language, name, lock=True)
            desired = self.validator.validate(language, current, name, description, variables, templates)
            plan = self.planner.plan(current, desired)
            self.writer.apply(language, current, desired)
        return self._result(name, False, plan)

    @staticmethod
    def _current(language: Language, name: str, *, lock: bool = False) -> Scaffolding | None:
        query = Scaffolding.objects.filter(language=language, name=name)
        return query.select_for_update().first() if lock else query.first()

    @staticmethod
    def _result(name: str, dry_run: bool, plan: ConvergencePlan) -> ConvergenceResult:
        groups = (plan["variables"], plan["templates"])
        changed = plan["scaffolding"] != "unchanged" or any(
            changes[operation] for changes in groups for operation in ("create", "update", "delete")
        )
        return {"name": name, "dry_run": dry_run, "changed": changed, "plan": plan}
