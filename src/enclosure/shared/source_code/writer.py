from pathlib import Path

from wireup import injectable

from .errors import SourceCodeError
from .package import CodePackage


@injectable
class CodePackageWriter:
    def write(
        self,
        package: CodePackage,
        destination: Path,
        *,
        overwrite: bool,
    ) -> None:
        root = destination.resolve()
        root.mkdir(parents=True, exist_ok=True)

        for path, contents in package.files.items():
            target = (root / path).resolve()
            if not target.is_relative_to(root):
                raise SourceCodeError(f"Code package file path escapes destination: {path}")
            if target.exists() and not overwrite:
                raise SourceCodeError(f"Destination already contains: {path}")

            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(contents, encoding="utf-8")
