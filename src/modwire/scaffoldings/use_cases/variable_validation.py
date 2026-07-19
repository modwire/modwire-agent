from typing import Any


from ..adapters.django.models.variable import VariableType
from .preview_errors import PreviewError, PreviewFailed


class VariableValidationService:
    json_types = {
        VariableType.STR: "string",
        VariableType.INT: "integer",
        VariableType.FLOAT: "number",
        VariableType.BOOL: "boolean",
        VariableType.LIST: "array",
        VariableType.DICT: "object",
    }

    def validate(self, variables, values: dict[str, Any]) -> dict[str, Any]:
        by_name = {variable.name: variable for variable in variables}
        errors = [
            PreviewError("unknown_variable", f"Unknown variable '{name}'.", {"field": name})
            for name in sorted(set(values) - set(by_name))
        ]
        context: dict[str, Any] = {}
        for name, variable in by_name.items():
            if name in values:
                value = values[name]
            elif variable.required:
                errors.append(PreviewError("required_variable", f"Variable '{name}' is required.", {"field": name}))
                continue
            else:
                value = variable.default_value
            if not self.matches(variable.type, value):
                errors.append(
                    PreviewError(
                        "invalid_variable_type",
                        f"Variable '{name}' must be of type '{variable.type}'.",
                        context={"field": name},
                    )
                )
            else:
                context[name] = value
        if errors:
            raise PreviewFailed(errors)
        return context

    @staticmethod
    def matches(variable_type: str, value: Any) -> bool:
        if variable_type == VariableType.FLOAT:
            return type(value) in {int, float}
        expected = {
            VariableType.STR: str,
            VariableType.INT: int,
            VariableType.BOOL: bool,
            VariableType.LIST: list,
            VariableType.DICT: dict,
        }.get(variable_type)
        return expected is not None and type(value) is expected
