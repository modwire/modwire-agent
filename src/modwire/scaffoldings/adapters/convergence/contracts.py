from dataclasses import dataclass
from typing import Literal, TypedDict

from pydantic import JsonValue

from ..django.models.scaffolding import Scaffolding
from ..django.models.template import Template
from ..django.models.variable import Variable


VariableSpec = TypedDict("VariableSpec", {"name": str, "type": str, "description": str, "default_value": JsonValue, "required": bool})
TemplateSpec = TypedDict("TemplateSpec", {"relative_path": str, "file_content": str, "write_mode": str})
ChangeSet = TypedDict("ChangeSet", {"create": list[str], "update": list[str], "delete": list[str]})
ConvergencePlan = TypedDict("ConvergencePlan", {"scaffolding": Literal["create", "update", "unchanged"], "variables": ChangeSet, "templates": ChangeSet})
ConvergenceResult = TypedDict("ConvergenceResult", {"id": str | None, "name": str, "dry_run": bool, "changed": bool, "plan": ConvergencePlan})


@dataclass(frozen=True)
class DesiredScaffolding:
    scaffolding: Scaffolding
    variables: tuple[Variable, ...]
    templates: tuple[Template, ...]
