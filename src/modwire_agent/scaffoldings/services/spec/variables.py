from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, TypeAdapter, field_validator


class VariableType(StrEnum):
    STRING = "string"
    INTEGER = "integer"
    NUMBER = "number"
    BOOLEAN = "boolean"
    ARRAY = "array"
    OBJECT = "object"


class BaseVariable(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    name: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, name: str) -> str:
        if not name.isidentifier():
            raise ValueError("Variable names must be valid Python-style identifiers.")
        return name


class StringVariable(BaseVariable):
    type: Literal[VariableType.STRING] = VariableType.STRING

    def validate_value(self, value: JsonValue) -> JsonValue:
        return TypeAdapter(str).validate_python(value, strict=True)


class IntegerVariable(BaseVariable):
    type: Literal[VariableType.INTEGER] = VariableType.INTEGER

    def validate_value(self, value: JsonValue) -> JsonValue:
        return TypeAdapter(int).validate_python(value, strict=True)


class NumberVariable(BaseVariable):
    type: Literal[VariableType.NUMBER] = VariableType.NUMBER

    def validate_value(self, value: JsonValue) -> JsonValue:
        return TypeAdapter(int | float).validate_python(value, strict=True)


class BooleanVariable(BaseVariable):
    type: Literal[VariableType.BOOLEAN] = VariableType.BOOLEAN

    def validate_value(self, value: JsonValue) -> JsonValue:
        return TypeAdapter(bool).validate_python(value, strict=True)


class ArrayVariable(BaseVariable):
    type: Literal[VariableType.ARRAY] = VariableType.ARRAY

    def validate_value(self, value: JsonValue) -> JsonValue:
        return TypeAdapter(list[JsonValue]).validate_python(value, strict=True)


class ObjectVariable(BaseVariable):
    type: Literal[VariableType.OBJECT] = VariableType.OBJECT

    def validate_value(self, value: JsonValue) -> JsonValue:
        return TypeAdapter(dict[str, JsonValue]).validate_python(value, strict=True)


Variable = Annotated[
    StringVariable
    | IntegerVariable
    | NumberVariable
    | BooleanVariable
    | ArrayVariable
    | ObjectVariable,
    Field(discriminator="type"),
]
