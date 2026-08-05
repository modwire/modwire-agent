from dataclasses import dataclass
from pathlib import Path

from wireup import injectable

from .errors import FilesystemError
from .package import FilesPackage


@injectable
@dataclass(frozen=True)
class FilesystemService:
    def read_directory(self, root_path: str) -> FilesPackage:
        root = Path(root_path)
        if not root.exists() or not root.is_dir():
            raise FilesystemError(f"Invalid project root: {root}")

        return FilesPackage(
            mapping={str(file.relative_to(root)): str(file) for file in root.rglob("*") if file.is_file()}
        )
