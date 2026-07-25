from typing import Literal

from ninja import Schema
from pydantic import JsonValue


class VariableFormPropertyOut(Schema):
    type: Literal["string", "integer", "number", "boolean", "array", "object"]
    description: str
    default: JsonValue
