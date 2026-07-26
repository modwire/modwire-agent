from typing import Literal

from ninja import Field, Schema
from pydantic import JsonValue

from modwire_agent.core.schema import StrictSchema

__all__ = ["StrictSchema"]


class VariableFormPropertyOut(Schema):
    type: Literal["string", "integer", "number", "boolean", "array", "object"]
    description: str
    default: JsonValue


class ScaffoldingFormSchemaOut(Schema):
    schema_uri: Literal["https://json-schema.org/draft/2020-12/schema"] = Field(alias="$schema")
    type: Literal["object"]
    properties: dict[str, VariableFormPropertyOut]
    required: list[str]
    allow_additional_properties: Literal[False] = Field(alias="additionalProperties")


class ScaffoldingConvergenceTemplateIn(StrictSchema):
    relative_path: str
    file_content: str
    write_mode: Literal["managed", "create_if_missing"] = "managed"


class ScaffoldingConvergenceVariableIn(StrictSchema):
    name: str
    type: Literal["str", "int", "float", "bool", "list", "dict"]
    description: str
    default_value: JsonValue
    required: bool = False


class ScaffoldingConvergenceIn(StrictSchema):
    language_id: str
    name: str
    description: str
    variables: list[ScaffoldingConvergenceVariableIn]
    templates: list[ScaffoldingConvergenceTemplateIn]
    dry_run: bool = True


class ConvergenceChangesOut(Schema):
    create: list[str]
    update: list[str]
    delete: list[str]


class ConvergencePlanOut(Schema):
    scaffolding: Literal["create", "update", "unchanged"]
    variables: ConvergenceChangesOut
    templates: ConvergenceChangesOut


type NullableIdentifier = str | None


class ScaffoldingConvergenceOut(Schema):
    id: NullableIdentifier
    name: str
    dry_run: bool
    changed: bool
    plan: ConvergencePlanOut


class ScaffoldingBundleTemplateOut(Schema):
    id: str
    relative_path: str
    file_content: str
    write_mode: Literal["managed", "create_if_missing"]


class ScaffoldingBundleVariableOut(Schema):
    id: str
    name: str
    type: Literal["str", "int", "float", "bool", "list", "dict"]
    description: str
    default_value: JsonValue
    required: bool


class ScaffoldingBundleOut(Schema):
    id: str
    name: str
    variables: list[ScaffoldingBundleVariableOut]
    templates: list[ScaffoldingBundleTemplateOut]


class PreviewErrorOut(Schema):
    code: Literal[
        "unknown_variable",
        "required_variable",
        "invalid_variable_type",
        "invalid_template_override",
        "duplicate_template_override",
        "jinja_syntax",
        "jinja_render",
        "invalid_rendered_path",
        "rendered_path_collision",
        "highlighting_failed",
    ]
    message: str
    details: dict[str, JsonValue] = Field(default_factory=dict)


class ScaffoldingPreviewErrorOut(Schema):
    errors: list[PreviewErrorOut]


class PreviewFileOut(Schema):
    template_id: str
    path: str
    source: str
    html: str
    language: str
    write_mode: Literal["managed", "create_if_missing"]


class TemplateOverrideIn(StrictSchema):
    template_id: str
    relative_path: str
    file_content: str


class ScaffoldingPreviewIn(StrictSchema):
    values: dict[str, JsonValue] = Field(default_factory=dict)
    template_overrides: list[TemplateOverrideIn] = Field(default_factory=list)


class ScaffoldingPreviewOut(Schema):
    files: list[PreviewFileOut]
