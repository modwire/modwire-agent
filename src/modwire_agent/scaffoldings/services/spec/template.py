from enum import StrEnum

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

from modwire_agent.shared import SourceCodePackage

from ...error import ScaffoldingError


class WriteMode(StrEnum):
    OVERWRITE = "overwrite"
    CREATE_IF_MISSING = "create_if_missing"


class Template(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    path: str
    content: str
    write_mode: WriteMode = WriteMode.OVERWRITE

    @field_validator("path")
    @classmethod
    def validate_path(cls, path: str) -> str:
        try:
            SourceCodePackage.model_validate(
                {"language": "", "package": {"files": {path: ""}}},
            )
        except ValidationError as error:
            raise ScaffoldingError(error.errors()[0]["msg"]) from error
        return path
