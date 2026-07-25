from modwire_agent.languages.domain.contracts import Language

from ..django.models.scaffolding import Scaffolding
from ..django.models.template import Template
from ..django.models.variable import Variable
from .contracts import DesiredScaffolding


class ScaffoldingAggregateWriter:
    def apply(
        self,
        language: Language,
        current: Scaffolding | None,
        desired: DesiredScaffolding,
    ) -> Scaffolding:
        scaffolding = self._scaffolding(language, current, desired.scaffolding)
        self._replace_variables(scaffolding, desired.variables)
        self._replace_templates(scaffolding, desired.templates)
        return scaffolding

    @staticmethod
    def _scaffolding(
        language: Language,
        current: Scaffolding | None,
        desired: Scaffolding,
    ) -> Scaffolding:
        if current is None:
            desired.language_id = language.id
            desired.save()
            return desired
        current.description = desired.description
        current.full_clean()
        current.save()
        return current

    @staticmethod
    def _replace_variables(scaffolding: Scaffolding, desired: tuple[Variable, ...]) -> None:
        existing = {item.name: item for item in Variable.objects.filter(scaffolding=scaffolding)}
        desired_names = {item.name for item in desired}
        Variable.objects.filter(scaffolding=scaffolding).exclude(name__in=desired_names).delete()
        for candidate in desired:
            instance = existing.get(candidate.name) or Variable(scaffolding=scaffolding)
            instance.name = candidate.name
            instance.type = candidate.type
            instance.description = candidate.description
            instance.default_value = candidate.default_value
            instance.required = candidate.required
            instance.full_clean()
            instance.save()

    @staticmethod
    def _replace_templates(scaffolding: Scaffolding, desired: tuple[Template, ...]) -> None:
        existing = {item.relative_path: item for item in Template.objects.filter(scaffolding=scaffolding)}
        desired_paths = {item.relative_path for item in desired}
        Template.objects.filter(scaffolding=scaffolding).exclude(relative_path__in=desired_paths).delete()
        for candidate in desired:
            instance = existing.get(candidate.relative_path) or Template(scaffolding=scaffolding)
            instance.relative_path = candidate.relative_path
            instance.file_content = candidate.file_content
            instance.write_mode = candidate.write_mode
            instance.full_clean()
            instance.save()
