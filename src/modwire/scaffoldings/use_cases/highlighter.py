from pathlib import PurePosixPath

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import TextLexer, get_lexer_for_filename
from pygments.util import ClassNotFound

from .preview_errors import PreviewError, PreviewFailed


class SyntaxHighlightingService:
    def highlight(self, path: str, source: str, *, template_id: str) -> tuple[str, str]:
        try:
            try:
                lexer = get_lexer_for_filename(PurePosixPath(path).name, source)
            except ClassNotFound:
                lexer = TextLexer()
            language = lexer.aliases[0] if lexer.aliases else "text"
            return highlight(source, lexer, HtmlFormatter(nowrap=True)), language
        except Exception as error:
            raise PreviewFailed(
                [
                    PreviewError(
                        "highlighting_failed",
                        str(error),
                        {"template_id": template_id, "template_path": path},
                    )
                ]
            ) from error
