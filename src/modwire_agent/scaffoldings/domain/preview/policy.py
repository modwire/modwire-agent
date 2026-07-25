from collections.abc import Iterable
from typing import Any

from ..code.package import CodePackage
from .errors import PreviewError, PreviewFailed


class ScaffoldingPreviewPolicy:
    json_types = {
        "str": "string",
        "int": "integer",
        "float": "number",
        "bool": "boolean",
        "list": "array",
        "dict": "object",
    }

    def values(self, variables: Iterable[Any], values: dict[str, Any]) -> dict[str, Any]:
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
                        {"field": name},
                    )
                )
            else:
                context[name] = value
        if errors:
            raise PreviewFailed(errors)
        return context

    def overrides(self, templates: Iterable[Any], requested: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        known = {str(template.id) for template in templates}
        result: dict[str, dict[str, Any]] = {}
        errors: list[PreviewError] = []
        for override in requested:
            template_id = override["template_id"]
            if template_id not in known:
                errors.append(
                    PreviewError(
                        "invalid_template_override",
                        f"Template '{template_id}' does not belong to this scaffolding.",
                        {"template_id": template_id},
                    )
                )
            elif template_id in result:
                errors.append(
                    PreviewError(
                        "duplicate_template_override",
                        f"Template '{template_id}' has more than one override.",
                        {"template_id": template_id},
                    )
                )
            else:
                result[template_id] = {key: value for key, value in override.items() if key != "template_id"}
        if errors:
            raise PreviewFailed(errors)
        return result

    def path(self, path: str, *, template_id: str, template_path: str) -> None:
        try:
            CodePackage._validate_file_path(path)
        except ValueError as error:
            raise PreviewFailed(
                [
                    PreviewError(
                        "invalid_rendered_path",
                        str(error),
                        {"template_id": template_id, "template_path": template_path},
                    )
                ]
            ) from error

    @staticmethod
    def collision(path: str, template_id: str, existing: dict[str, str]) -> None:
        for other_path, other_id in existing.items():
            if path == other_path:
                message = f"Rendered path '{path}' is produced by multiple templates."
            elif path.startswith(other_path + "/") or other_path.startswith(path + "/"):
                message = f"Rendered paths '{path}' and '{other_path}' conflict as a file and directory."
            else:
                continue
            raise PreviewFailed(
                [
                    PreviewError(
                        "rendered_path_collision",
                        message,
                        {"template_id": other_id, "template_path": other_path},
                    ),
                    PreviewError(
                        "rendered_path_collision",
                        message,
                        {"template_id": template_id, "template_path": path},
                    ),
                ]
            )

    @staticmethod
    def matches(variable_type: str, value: Any) -> bool:
        if variable_type == "float":
            return type(value) in {int, float}
        expected = {"str": str, "int": int, "bool": bool, "list": list, "dict": dict}.get(variable_type)
        return expected is not None and type(value) is expected
