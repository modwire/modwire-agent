from dataclasses import dataclass, field
from typing import Any

from .compiler import ShapeCompiler
from .schema import Schema
from .validator import JsonSchemaValidator


@dataclass(frozen=True)
class JsonSchemaService:
    compiler: ShapeCompiler = field(default_factory=ShapeCompiler)
    validator: JsonSchemaValidator = field(default_factory=JsonSchemaValidator)

    def define(self, shape: dict[str, Any]) -> Schema:
        document = self.compiler.compile(shape)
        self.validator.require_valid_schema(document)
        return Schema(document, self.validator)

    def load(self, document: dict[str, Any]) -> Schema:
        canonical_document = {"$schema": "https://json-schema.org/draft/2020-12/schema", **document}
        self.validator.require_valid_schema(canonical_document)
        return Schema(canonical_document, self.validator)
