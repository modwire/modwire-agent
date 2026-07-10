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
            raise ValueError("Code package file path must use POSIX separators.")
        if path.startswith("/"):
            raise ValueError("Code package file path must be relative.")
        if path.endswith("/"):
            raise ValueError("Code package file path must point to a file.")

        parts = path.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            raise ValueError(
                "Code package file path cannot contain empty, current, "
                "or parent segments."
            )
