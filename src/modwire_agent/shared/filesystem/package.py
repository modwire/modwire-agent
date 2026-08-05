from pydantic import BaseModel


class FilesPackage(BaseModel):
    mapping: dict[str, str]

    @property
    def is_empty(self) -> bool:
        return not self.mapping

    def has_path(self, path: str) -> bool:
        return path in self.mapping
