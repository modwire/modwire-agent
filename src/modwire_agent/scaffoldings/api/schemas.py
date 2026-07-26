from ninja import Schema, Field
from pydantic import JsonValue, ConfigDict


class StrictSchema(Schema):
    model_config = ConfigDict(extra="forbid")


class NewScaffolding(StrictSchema):
    language: str
    name: str
    description: str


class Template(StrictSchema):
    relative_path: str
    file_content: str
    write_mode: str


class UpdateTemplate(StrictSchema):
    id: str


class Variable(StrictSchema):
    name: str
    shape: str
    description: str
    default_value: JsonValue
    required: bool


class UpdateVariable(Variable):
    id: str


class Scaffolding(Template):
    id: str
    templates: list[UpdateTemplate] = Field()
    variables: list[UpdateVariable] = Field()


class Parameter(StrictSchema):
    name: str
    value: JsonValue


class GenerateSourceCode(StrictSchema):
    parameters: list[Parameter]
    target_root: str = ""


class SourceCode(StrictSchema):
    files: dict[str, str]
