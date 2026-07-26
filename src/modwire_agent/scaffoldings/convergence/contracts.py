from dataclasses import dataclass

from ..models import Scaffolding, Template, Variable


@dataclass(frozen=True)
class DesiredScaffolding:
    scaffolding: Scaffolding
    variables: tuple[Variable, ...]
    templates: tuple[Template, ...]
