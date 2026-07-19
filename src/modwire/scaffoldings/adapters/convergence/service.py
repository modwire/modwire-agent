from dataclasses import dataclass

from django.db import transaction

from modwire.languages.domain.contracts import Language
from modwire.languages.use_cases import LanguageCatalogService

from ..django.models.scaffolding import Scaffolding
from ...ports.scaffolding_convergence import ScaffoldingConvergence
from .contracts import ConvergencePlan, ConvergenceResult, TemplateSpec, VariableSpec
from .planner import ScaffoldingConvergencePlanner
from .validator import ScaffoldingAggregateValidator
from .writer import ScaffoldingAggregateWriter


@dataclass(frozen=True)
class DjangoScaffoldingConvergence(ScaffoldingConvergence):
    catalog: LanguageCatalogService
    validator: ScaffoldingAggregateValidator
    planner: ScaffoldingConvergencePlanner
    writer: ScaffoldingAggregateWriter

    def execute(self, request: dict[str, object]) -> ConvergenceResult:
        language_id = str(request["language_id"])
        name = str(request["name"])
        description = str(request["description"])
        variables = request["variables"]
        templates = request["templates"]
        dry_run = bool(request["dry_run"])
        language = self.catalog.find(language_id)
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
        query = Scaffolding.objects.filter(language_id=language.id, name=name)
        return query.select_for_update().first() if lock else query.first()

    @staticmethod
    def _result(name: str, dry_run: bool, plan: ConvergencePlan) -> ConvergenceResult:
        groups = (plan["variables"], plan["templates"])
        changed = plan["scaffolding"] != "unchanged" or any(
            changes[operation] for changes in groups for operation in ("create", "update", "delete")
        )
        return {"name": name, "dry_run": dry_run, "changed": changed, "plan": plan}
