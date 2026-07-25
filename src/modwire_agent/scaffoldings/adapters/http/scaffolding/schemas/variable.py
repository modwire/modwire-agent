from typing import Literal

from pydantic import JsonValue

from modwire_agent.scaffoldings.adapters.http.schema import StrictSchema


class ScaffoldingConvergenceVariableIn(StrictSchema):
    name: str
    type: Literal["str", "int", "float", "bool", "list", "dict"]
    description: str
    default_value: JsonValue
    required: bool = False
