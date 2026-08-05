from ninja import Schema
from pydantic import JsonValue

from ..services.spec.model import ScaffoldingSpec


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
