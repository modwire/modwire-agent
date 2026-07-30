import json
import math
from collections.abc import Mapping
from typing import Any

from wireup import injectable

from .errors import InvalidShape, JsonSchemaIssue


@injectable
class ShapeCompiler:
    def compile(self, shape: dict[str, Any]) -> dict[str, Any]:
        return {"$schema": "https://json-schema.org/draft/2020-12/schema", **self._object(shape, ())}

    def _object(self, shape: Any, path: tuple[str | int, ...]) -> dict[str, Any]:
        if not isinstance(shape, Mapping):
            self._invalid(path, "An object shape must be a mapping.")

        properties: dict[str, Any] = {}
        required: list[str] = []
        names: set[str] = set()
        for key, value in shape.items():
            if not isinstance(key, str):
                self._invalid(path, "Object property names must be strings.")
            name, optional = self._property_name(key, path)
            if name in names:
                self._invalid(path + (key,), f"Property '{name}' is declared more than once.")
            names.add(name)
            properties[name] = self._schema(value, path + (name,))
            if not optional:
                required.append(name)

        result: dict[str, Any] = {
            "type": "object",
            "properties": properties,
            "additionalProperties": False,
        }
        if required:
            result["required"] = required
        return result

    def _schema(self, shape: Any, path: tuple[str | int, ...]) -> dict[str, Any]:
        if isinstance(shape, Mapping):
            return self._object(shape, path)
        if isinstance(shape, list):
            if len(shape) != 1:
                self._invalid(path, "An array shape must contain exactly one item shape.")
            return {"type": "array", "items": self._schema(shape[0], path + (0,))}
        if isinstance(shape, tuple):
            return self._enum(shape, path)
        primitive_types = {str: "string", int: "integer", float: "number", bool: "boolean", type(None): "null"}
        if isinstance(shape, type) and shape in primitive_types:
            return {"type": primitive_types[shape]}
        self._invalid(path, f"Unsupported shape: {shape!r}.")

    def _enum(self, values: tuple[Any, ...], path: tuple[str | int, ...]) -> dict[str, Any]:
        if not values:
            self._invalid(path, "An enum shape must contain at least one value.")
        if any(type(value) not in {str, int, float, bool, type(None)} for value in values):
            self._invalid(path, "Enum values must be JSON primitive values.")
        if any(type(value) is float and not math.isfinite(value) for value in values):
            self._invalid(path, "Enum values must be finite JSON numbers.")
        encoded_values = [json.dumps(value, sort_keys=True, allow_nan=False) for value in values]
        if len(encoded_values) != len(set(encoded_values)):
            self._invalid(path, "Enum values must be unique.")
        return {"enum": list(values)}

    def _property_name(self, key: str, path: tuple[str | int, ...]) -> tuple[str, bool]:
        optional = key.endswith("?")
        name = key[:-1] if optional else key
        if not name:
            self._invalid(path + (key,), "Object property names cannot be empty.")
        if "?" in name:
            self._invalid(path + (key,), "The optional property marker may appear only once at the end of a name.")
        return name, optional

    @staticmethod
    def _invalid(path: tuple[str | int, ...], message: str) -> None:
        raise InvalidShape((JsonSchemaIssue(path, message),))
