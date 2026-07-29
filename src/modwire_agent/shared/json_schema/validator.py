from collections.abc import Mapping
from typing import Any

from jsonschema import Draft202012Validator, SchemaError
from jsonschema.exceptions import ValidationError

from .errors import InvalidSchema, InvalidValue, JsonSchemaIssue


class JsonSchemaValidator:
    def require_valid_schema(self, document: Mapping[str, Any]) -> None:
        schema_uri = document.get("$schema", "https://json-schema.org/draft/2020-12/schema")
        if schema_uri != "https://json-schema.org/draft/2020-12/schema":
            raise InvalidSchema((JsonSchemaIssue(("$schema",), "Schemas must use JSON Schema Draft 2020-12."),))
        try:
            Draft202012Validator.check_schema(document)
        except SchemaError as error:
            raise InvalidSchema((self._issue(error),)) from error

    def require_valid_value(self, document: Mapping[str, Any], value: Any) -> None:
        validator = Draft202012Validator(document)
        errors = sorted(validator.iter_errors(value), key=lambda error: str(list(error.absolute_path)))
        if errors:
            raise InvalidValue(tuple(self._issue(error) for error in errors))

    @staticmethod
    def _issue(error: SchemaError | ValidationError) -> JsonSchemaIssue:
        return JsonSchemaIssue(tuple(error.absolute_path), error.message)
