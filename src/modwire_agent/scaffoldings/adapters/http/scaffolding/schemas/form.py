from typing import Literal

from ninja import Field, Schema

from .form_property import VariableFormPropertyOut


class ScaffoldingFormSchemaOut(Schema):
    schema_uri: Literal["https://json-schema.org/draft/2020-12/schema"] = Field(alias="$schema")
    type: Literal["object"]
    properties: dict[str, VariableFormPropertyOut]
    required: list[str]
    allow_additional_properties: Literal[False] = Field(alias="additionalProperties")
