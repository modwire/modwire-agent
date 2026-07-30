from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory

from wireup import injectable

from .code_map import QueryableCodeMapReader
from .errors import SourceCodeError


@injectable
@dataclass(frozen=True)
class SourceExtractionService:
    reader: QueryableCodeMapReader

    def validate(self, language_id: str, path: str, content: str) -> None:
        relative_path = PurePosixPath(path)
        with TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source = (root / relative_path).resolve()
            if not source.is_relative_to(root):
                raise SourceCodeError(f"Source path escapes extraction root: {path!r}")
            source.parent.mkdir(parents=True, exist_ok=True)
            source.write_text(content, encoding="utf-8")
            try:
                self.reader.read(root, language_id)
            except RuntimeError as error:
                raise SourceCodeError(f"Invalid {language_id} source: {path!r}.") from error
