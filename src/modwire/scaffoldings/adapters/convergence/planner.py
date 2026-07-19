from collections.abc import Callable

from ..django.models.scaffolding import Scaffolding
from ..django.models.template import Template
from ..django.models.variable import Variable
from .contracts import ChangeSet, ConvergencePlan, DesiredScaffolding


class ScaffoldingConvergencePlanner:
    def plan(self, current: Scaffolding | None, desired: DesiredScaffolding) -> ConvergencePlan:
        return {
            "scaffolding": "create"
            if current is None
            else ("update" if current.description != desired.scaffolding.description else "unchanged"),
            "variables": self._variable_changes(current, desired.variables),
            "templates": self._template_changes(current, desired.templates),
        }

    @staticmethod
    def _variable_changes(current: Scaffolding | None, desired: tuple[Variable, ...]) -> ChangeSet:
        existing = {item.name: item for item in current.variables.all()} if current else {}
        requested = {item.name: item for item in desired}
        return ScaffoldingConvergencePlanner._changes(
            existing,
            requested,
            lambda before, after: (
                (
                    before.type,
                    before.description,
                    before.default_value,
                    before.required,
                )
                != (
                    after.type,
                    after.description,
                    after.default_value,
                    after.required,
                )
            ),
        )

    @staticmethod
    def _template_changes(current: Scaffolding | None, desired: tuple[Template, ...]) -> ChangeSet:
        existing = {item.relative_path: item for item in current.templates.all()} if current else {}
        requested = {item.relative_path: item for item in desired}
        return ScaffoldingConvergencePlanner._changes(
            existing,
            requested,
            lambda before, after: (before.file_content, before.write_mode) != (after.file_content, after.write_mode),
        )

    @staticmethod
    def _changes[T](
        current: dict[str, T],
        desired: dict[str, T],
        changed: Callable[[T, T], bool],
    ) -> ChangeSet:
        current_keys = set(current)
        desired_keys = set(desired)
        return {
            "create": sorted(desired_keys - current_keys),
            "update": sorted(key for key in current_keys & desired_keys if changed(current[key], desired[key])),
            "delete": sorted(current_keys - desired_keys),
        }
