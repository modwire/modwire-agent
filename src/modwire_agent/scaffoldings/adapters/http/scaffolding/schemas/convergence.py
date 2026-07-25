from modwire_agent.scaffoldings.adapters.http.schema import StrictSchema

from .template import ScaffoldingConvergenceTemplateIn
from .variable import ScaffoldingConvergenceVariableIn


class ScaffoldingConvergenceIn(StrictSchema):
    language_id: str
    name: str
    description: str
    variables: list[ScaffoldingConvergenceVariableIn]
    templates: list[ScaffoldingConvergenceTemplateIn]
    dry_run: bool = True
