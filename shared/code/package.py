from pathlib import Path
from typing import Self
from pydantic import BaseModel, field_validator


class CodePackage(BaseModel):
    files: dict[str, str]

    @field_validator("files")
    @classmethod
    def validate_file_paths(cls, files: dict[str, str]) -> dict[str, str]:
        for path in files:
            cls._validate_file_path(path)
        return files

    @staticmethod
    def _validate_file_path(path: str) -> None:
        if not path:
            raise ValueError("Code package file path cannot be empty.")

        if "\\" in path:
            raise ValueError(
                f"Code package path must use POSIX separators: {path!r}"
            )

        if path.startswith("/"):
            raise ValueError(
                f"Code package path must be relative: {path!r}"
            )

        if path.endswith("/"):
            raise ValueError(
                f"Code package path must point to a file: {path!r}"
            )

        parts = path.split("/")

        if any(part in {"", ".", ".."} for part in parts):
            raise ValueError(
                f"Code package path contains an invalid segment: {path!r}"
            )

    @classmethod
    def from_directory(cls, root: Path) -> Self:
        root = root.resolve()

        if not root.is_dir():
            raise ValueError(f"Code package root is not a directory: {root}")

        files: dict[str, str] = {}

        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                raise ValueError(
                    f"Symbolic links are not supported: {path}"
                )

            if not path.is_file():
                continue

            relative_path = path.relative_to(root).as_posix()
            files[relative_path] = path.read_text(encoding="utf-8")

        return cls(files=files)

    def write_to_directory(self, root: Path) -> None:
        root.mkdir(parents=True, exist_ok=True)
        root = root.resolve()

        for relative_path, content in self.files.items():
            self._validate_file_path(relative_path)

            destination = root.joinpath(*relative_path.split("/"))
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")