import re
from typing import Any

from jinja2 import StrictUndefined, TemplateError, TemplateSyntaxError
from jinja2.sandbox import SandboxedEnvironment

from ...domain.preview import PreviewError, PreviewFailed


class SandboxedTemplateRenderer:
    def __init__(self):
        self.environment = SandboxedEnvironment(
            undefined=StrictUndefined,
            autoescape=False,
            keep_trailing_newline=True,
        )
        self.environment.filters.update(
            snake=lambda value: "_".join(self._words(value)),
            kebab=lambda value: "-".join(self._words(value)),
            camel=lambda value: self._camel(value),
            pascal=lambda value: "".join(word.capitalize() for word in self._words(value)),
            title=lambda value: " ".join(word.capitalize() for word in self._words(value)),
        )

    @staticmethod
    def _words(value: Any) -> list[str]:
        text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", str(value))
        text = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", text)
        return [word.lower() for word in re.findall(r"[A-Za-z0-9]+", text)]

    @staticmethod
    def _camel(value: Any) -> str:
        words = SandboxedTemplateRenderer._words(value)
        return "" if not words else words[0] + "".join(word.capitalize() for word in words[1:])

    def render(self, source: str, context: dict[str, Any], *, template_id: str, template_path: str) -> str:
        try:
            return self.environment.from_string(source).render(context)
        except TemplateError as error:
            context = {
                "template_id": template_id,
                "template_path": template_path,
                **({"line": error.lineno} if getattr(error, "lineno", None) is not None else {}),
            }
            code = "jinja_syntax" if isinstance(error, TemplateSyntaxError) else "jinja_render"
            raise PreviewFailed([PreviewError(code, str(error), context)]) from error
