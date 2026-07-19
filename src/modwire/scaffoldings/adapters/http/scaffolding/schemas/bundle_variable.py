from typing import Literal

from ninja import Schema
from pydantic import JsonValue


class ScaffoldingBundleVariableOut(Schema):
    id: str
    name: str
    type: Literal["str", "int", "float", "bool", "list", "dict"]
    description: str
    default_value: JsonValue
    required: bool
