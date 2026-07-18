from typing import Any

from wireup import injectable

from .highlighter import SyntaxHighlightingService
from .preview_errors import PreviewError, PreviewFailed
from .renderer import SandboxedTemplateRenderer
from .scaffolding import ScaffoldingService
from .variable_validation import VariableValidationService


@injectable
class ScaffoldingPreviewService:
    def __init__(
        self,
        scaffoldings: ScaffoldingService,
        validation: VariableValidationService,
        renderer: SandboxedTemplateRenderer,
        highlighter: SyntaxHighlightingService,
    ):
        self.scaffoldings = scaffoldings
        self.validation = validation
        self.renderer = renderer
        self.highlighter = highlighter

    def preview(
        self,
        scaffolding_id: str,
        values: dict[str, Any],
        template_overrides: list[dict[str, Any]],
    ) -> dict[str, list[dict[str, str]]]:
        scaffolding = self.scaffoldings.get(scaffolding_id)
        templates = list(scaffolding.templates.order_by("relative_path"))
        variables = list(scaffolding.variables.order_by("name"))
        context = self.validation.validate(variables, values)
        overrides = self._overrides(templates, template_overrides)

        rendered = []
        paths: dict[str, str] = {}
        for template in templates:
            template_id = str(template.id)
            override = overrides.get(template_id, {})
            source_path = override.get("relative_path", template.relative_path)
            source = override.get("file_content", template.file_content)
            path = self.renderer.render(
                source_path,
                context,
                template_id=template_id,
                template_path=source_path,
            )
            self.renderer.validate_path(path, template_id=template_id, template_path=source_path)
            self._validate_collision(path, template_id, paths)
            paths[path] = template_id
            rendered_source = self.renderer.render(
                source,
                context,
                template_id=template_id,
                template_path=source_path,
            )
            html, language = self.highlighter.highlight(path, rendered_source, template_id=template_id)
            rendered.append(
                {
                    "template_id": template_id,
                    "path": path,
                    "source": rendered_source,
                    "html": html,
                    "language": language,
                    "write_mode": template.write_mode,
                }
            )
        return {"files": sorted(rendered, key=lambda item: item["path"])}

    @staticmethod
    def _overrides(templates, requested: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        known = {str(template.id) for template in templates}
        result = {}
        errors = []
        for override in requested:
            template_id = override["template_id"]
            if template_id not in known:
                errors.append(
                    PreviewError(
                        "invalid_template_override",
                        f"Template '{template_id}' does not belong to this scaffolding.",
                        context={"template_id": template_id},
                    )
                )
            elif template_id in result:
                errors.append(
                    PreviewError(
                        "duplicate_template_override",
                        f"Template '{template_id}' has more than one override.",
                        context={"template_id": template_id},
                    )
                )
            else:
                result[template_id] = {key: value for key, value in override.items() if key != "template_id"}
        if errors:
            raise PreviewFailed(errors)
        return result

    @staticmethod
    def _validate_collision(path: str, template_id: str, existing: dict[str, str]) -> None:
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
