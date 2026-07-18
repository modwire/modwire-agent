from collections import Counter
from typing import Literal

from django.core.exceptions import ValidationError
from wireup import injectable

from modwire.shared import languages

from ...models.scaffolding import Scaffolding
from ...models.template import Template
from ...models.variable import Variable
from .contracts import DesiredScaffolding, TemplateSpec, VariableSpec


@injectable
class ScaffoldingAggregateValidator:
    def validate(
        self,
        language: languages.Language,
        current: Scaffolding | None,
        name: str,
        description: str,
        variables: list[VariableSpec],
        templates: list[TemplateSpec],
    ) -> DesiredScaffolding:
        self._reject_duplicates("variables", "name", [item["name"] for item in variables])
        self._reject_duplicates("templates", "relative_path", [item["relative_path"] for item in templates])

        scaffolding = Scaffolding(language_id=language.id, name=name, description=description)
        if current:
            scaffolding.id = current.id
        scaffolding._state.adding = current is None
        scaffolding.full_clean()

        current_variables = {item.name: item for item in current.variables.all()} if current else {}
        desired_variables = tuple(
            self._variable(scaffolding, current_variables.get(spec["name"]), spec) for spec in variables
        )
        current_templates = {item.relative_path: item for item in current.templates.all()} if current else {}
        desired_templates = tuple(
            self._template(scaffolding, current_templates.get(spec["relative_path"]), spec) for spec in templates
        )
        return DesiredScaffolding(scaffolding, desired_variables, desired_templates)

    @staticmethod
    def _variable(scaffolding: Scaffolding, current: Variable | None, spec: VariableSpec) -> Variable:
        variable = Variable(
            scaffolding=scaffolding,
            name=spec["name"],
            type=spec["type"],
            description=spec["description"],
            default_value=spec["default_value"],
            required=spec["required"],
        )
        if current:
            variable.id = current.id
        variable._state.adding = current is None
        variable.full_clean(exclude={"scaffolding"})
        return variable

    @staticmethod
    def _template(scaffolding: Scaffolding, current: Template | None, spec: TemplateSpec) -> Template:
        template = Template(
            scaffolding=scaffolding,
            relative_path=spec["relative_path"],
            file_content=spec["file_content"],
            write_mode=spec["write_mode"],
        )
        if current:
            template.id = current.id
        template._state.adding = current is None
        template.full_clean(exclude={"scaffolding"})
        return template

    @staticmethod
    def _reject_duplicates(collection: str, key: Literal["name", "relative_path"], values: list[str]) -> None:
        duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
        if duplicates:
            raise ValidationError({collection: [f"Duplicate {key}: {value}" for value in duplicates]})
