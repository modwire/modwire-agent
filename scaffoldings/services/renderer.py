import re
from typing import Any

from jinja2 import StrictUndefined, TemplateError, TemplateSyntaxError
from jinja2.sandbox import SandboxedEnvironment
from wireup import injectable

from shared.code.package import CodePackage

from .preview_errors import PreviewError, PreviewFailed


def _words(value: Any) -> list[str]:
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(value))
    text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)
    return [word.lower() for word in re.findall(r"[A-Za-z0-9]+", text)]


@injectable
class SandboxedTemplateRenderer:
    def __init__(self):
        self.environment = SandboxedEnvironment(undefined=StrictUndefined, autoescape=False)
        self.environment.filters.update(
            snake=lambda value: "_".join(_words(value)),
            kebab=lambda value: "-".join(_words(value)),
            camel=lambda value: self._camel(value),
            pascal=lambda value: "".join(word.capitalize() for word in _words(value)),
            title=lambda value: " ".join(word.capitalize() for word in _words(value)),
        )

    @staticmethod
    def _camel(value: Any) -> str:
        words = _words(value)
        return "" if not words else words[0] + "".join(word.capitalize() for word in words[1:])

    def render(self, source: str, context: dict[str, Any], *, template_id: str, template_path: str) -> str:
        try:
            return self.environment.from_string(source).render(context)
        except TemplateError as error:
            raise PreviewFailed(
                [
                    PreviewError(
                        code="jinja_syntax" if isinstance(error, TemplateSyntaxError) else "jinja_render",
                        message=str(error),
                        context={
                            "template_id": template_id,
                            "template_path": template_path,
                            **({"line": error.lineno} if getattr(error, "lineno", None) is not None else {}),
                        },
                    )
                ]
            ) from error

    def validate_path(self, path: str, *, template_id: str, template_path: str) -> None:
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
