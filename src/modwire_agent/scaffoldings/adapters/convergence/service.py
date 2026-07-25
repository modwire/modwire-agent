from dataclasses import dataclass

from django.db import transaction

from modwire_agent.languages.domain.contracts import Language
from modwire_agent.languages.use_cases.language.get_language import GetLanguage

from ...ports.scaffolding_convergence import ScaffoldingConvergence
from ..django.models.scaffolding import Scaffolding
from .convergence_plan import ConvergencePlan
from .convergence_result import ConvergenceResult
from .planner import ScaffoldingConvergencePlanner
from .validator import ScaffoldingAggregateValidator
from .writer import ScaffoldingAggregateWriter


@dataclass(frozen=True)
class DjangoScaffoldingConvergence(ScaffoldingConvergence):
    languages: GetLanguage
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
        language = self.languages.execute(language_id)
        current = self._current(language, name, False)
        desired = self.validator.validate(language, current, name, description, variables, templates)
        plan = self.planner.plan(current, desired)
        if dry_run:
            return self._result(None, name, True, plan)

        with transaction.atomic():
            current = self._current(language, name, True)
            desired = self.validator.validate(language, current, name, description, variables, templates)
            plan = self.planner.plan(current, desired)
            scaffolding = self.writer.apply(language, current, desired)
        return self._result(scaffolding.id, name, False, plan)

    @staticmethod
    def _current(language: Language, name: str, lock: bool) -> Scaffolding | None:
        query = Scaffolding.objects.filter(language_id=language.id, name=name)
        return query.select_for_update().first() if lock else query.first()

    @staticmethod
    def _result(
        identifier: str | None,
        name: str,
        dry_run: bool,
        plan: ConvergencePlan,
    ) -> ConvergenceResult:
        groups = (plan["variables"], plan["templates"])
        changed = plan["scaffolding"] != "unchanged" or any(
            changes[operation] for changes in groups for operation in ("create", "update", "delete")
        )
        return {
            "id": identifier,
            "name": name,
            "dry_run": dry_run,
            "changed": changed,
            "plan": plan,
        }
