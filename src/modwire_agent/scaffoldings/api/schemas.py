from ninja import Schema
from pydantic import JsonValue, ConfigDict


class StrictSchema(Schema):
    model_config = ConfigDict(extra="forbid")


class NewScaffolding(StrictSchema):
    language: str
    name: str
    description: str


class Scaffolding(StrictSchema):
    id: str


class NewTemplate(StrictSchema):
    relative_path: str
    file_content: str
    write_mode: str


class Template(StrictSchema):
    id: str


class NewVariable(StrictSchema):
    name: str
    shape: str
    descrription: str
    default_value: JsonValue
    required: bool


class Variable(NewVariable):
    id: str


class Parameter(NewVariable):
    name: str
    value: JsonValue


class GenerateSourceCode(StrictSchema):
    scaffold_id: str
    parameters: list[Parameter]


class SourceCode(StrictSchema):
    files: dict[str, str]
