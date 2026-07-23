from typing import TypedDict

from pydantic import JsonValue


class VariableSpec(TypedDict):
    name: str
    type: str
    description: str
    default_value: JsonValue
    required: bool
