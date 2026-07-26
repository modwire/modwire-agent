from ninja import Schema
from pydantic import JsonValue


class Variable(Schema):
    name: str
    shape: str
    description: str
    default_value: JsonValue
    required: bool


class Template(Schema):
    relative_path: str
    file_content: str
    write_mode: str


class ScaffoldingSpec(Schema):
    variables: list[Variable]
    templates: list[Template]


class ScaffoldingInput(Schema):
    language_id: str
    name: str
    description: str
    spec: ScaffoldingSpec


class ScaffoldingSummary(Schema):
    id: str
    language_id: str
    name: str
    description: str


class Scaffolding(ScaffoldingSummary):
    spec: ScaffoldingSpec


class GenerateSourceCode(Schema):
    parameters: dict[str, JsonValue]


class Rendering(Schema):
    files: dict[str, str]
