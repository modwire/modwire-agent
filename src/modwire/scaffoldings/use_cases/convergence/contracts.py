from dataclasses import dataclass
from typing import Literal, TypedDict

from pydantic import JsonValue

from ...adapters.django.models.scaffolding import Scaffolding
from ...adapters.django.models.template import Template
from ...adapters.django.models.variable import Variable


class VariableSpec(TypedDict):
    name: str
    type: str
    description: str
    default_value: JsonValue
    required: bool


class TemplateSpec(TypedDict):
    relative_path: str
    file_content: str
    write_mode: str


class ChangeSet(TypedDict):
    create: list[str]
    update: list[str]
    delete: list[str]


class ConvergencePlan(TypedDict):
    scaffolding: Literal["create", "update", "unchanged"]
    variables: ChangeSet
    templates: ChangeSet


class ConvergenceResult(TypedDict):
    name: str
    dry_run: bool
    changed: bool
    plan: ConvergencePlan


@dataclass(frozen=True)
class DesiredScaffolding:
    scaffolding: Scaffolding
    variables: tuple[Variable, ...]
    templates: tuple[Template, ...]
