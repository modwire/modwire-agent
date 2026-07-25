from dataclasses import dataclass

from ..django.models.scaffolding import Scaffolding
from ..django.models.template import Template
from ..django.models.variable import Variable


@dataclass(frozen=True)
class DesiredScaffolding:
    scaffolding: Scaffolding
    variables: tuple[Variable, ...]
    templates: tuple[Template, ...]
