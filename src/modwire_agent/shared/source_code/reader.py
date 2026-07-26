from dataclasses import dataclass
from pathlib import Path

from wireup import injectable

from .package import CodePackage


@injectable
@dataclass(frozen=True)
class CodePackageReader:
    def read_package(self, root: Path, extensions: list[str] | None = None) -> CodePackage:
        root = root.resolve()
        assert root.is_dir()

        files: dict[str, str] = {}

        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symbolic links are not supported: {path}")

            if not path.is_file():
                continue

            relative_path = path.relative_to(root).as_posix()
            if extensions and not any(relative_path.endswith(extension) for extension in extensions):
                continue
            files[relative_path] = path.read_text(encoding="utf-8")

        return CodePackage(files=files)
