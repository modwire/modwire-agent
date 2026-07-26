from dataclasses import dataclass
from pathlib import Path

from .package import CodePackage


@dataclass(frozen=True)
class CodePackageReader:
    def read_package(self, root: Path, extensions: list[str]) -> CodePackage:
        root = root.resolve()
        assert root.is_dir()

        files: dict[str, str] = {}

        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"Symbolic links are not supported: {path}")

            if not path.is_file():
                continue

            relative_path = path.relative_to(root).as_posix()
            files[relative_path] = path.read_text(encoding="utf-8")

        return CodePackage(files=files)
