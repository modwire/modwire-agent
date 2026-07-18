from typing import Literal

from ninja import Field, Schema
from pydantic import JsonValue

from modwire.shared.api.schema import StrictSchema

from ...models.template import Template


class ScaffoldingConvergenceVariableIn(StrictSchema):
    name: str
    type: Literal["str", "int", "float", "bool", "list", "dict"]
    description: str
    default_value: JsonValue
    required: bool = False


class ScaffoldingConvergenceTemplateIn(StrictSchema):
    relative_path: str
    file_content: str
    write_mode: Template.WriteMode = Template.WriteMode.MANAGED


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


class ScaffoldingConvergenceOut(Schema):
    name: str
    dry_run: bool
    changed: bool
    plan: ConvergencePlanOut


class TemplateOverrideIn(StrictSchema):
    template_id: str
    relative_path: str
    file_content: str


class ScaffoldingPreviewIn(StrictSchema):
    values: dict[str, JsonValue] = Field(default_factory=dict)
    template_overrides: list[TemplateOverrideIn] = Field(default_factory=list)


class PreviewFileOut(Schema):
    template_id: str
    path: str
    source: str
    html: str
    language: str
    write_mode: Template.WriteMode


class ScaffoldingPreviewOut(Schema):
    files: list[PreviewFileOut]


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


class ScaffoldingBundleVariableOut(Schema):
    id: str
    name: str
    type: Literal["str", "int", "float", "bool", "list", "dict"]
    description: str
    default_value: JsonValue
    required: bool


class ScaffoldingBundleTemplateOut(Schema):
    id: str
    relative_path: str
    file_content: str
    write_mode: Template.WriteMode


class ScaffoldingBundleOut(Schema):
    id: str
    name: str
    variables: list[ScaffoldingBundleVariableOut]
    templates: list[ScaffoldingBundleTemplateOut]
