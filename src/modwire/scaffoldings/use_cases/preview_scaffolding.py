from typing import Any

from ..adapters.preview import SandboxedTemplateRenderer, SyntaxHighlightingService
from ..domain.preview import ScaffoldingPreviewPolicy
from .get_scaffolding import GetScaffolding


class PreviewScaffolding:
    def __init__(
        self,
        get_scaffolding: GetScaffolding,
        policy: ScaffoldingPreviewPolicy,
        renderer: SandboxedTemplateRenderer,
        highlighter: SyntaxHighlightingService,
    ):
        self.get_scaffolding = get_scaffolding
        self.policy = policy
        self.renderer = renderer
        self.highlighter = highlighter

    def execute(
        self,
        scaffolding_id: str,
        values: dict[str, Any],
        template_overrides: list[dict[str, Any]],
    ) -> dict[str, list[dict[str, str]]]:
        scaffolding = self.get_scaffolding.execute(scaffolding_id)
        templates = list(scaffolding.templates.order_by("relative_path"))
        context = self.policy.values(scaffolding.variables.order_by("name"), values)
        overrides = self.policy.overrides(templates, template_overrides)
        rendered: list[dict[str, str]] = []
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
            self.policy.path(path, template_id=template_id, template_path=source_path)
            self.policy.collision(path, template_id, paths)
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
