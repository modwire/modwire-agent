from enum import StrEnum

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator, model_validator

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

    @model_validator(mode="after")
    def validate_jinja_content_path(self) -> "Template":
        if not self.path.endswith(".jinja") and any(token in self.content for token in ("{{", "{%", "{#")):
            raise ScaffoldingError("Template content uses Jinja syntax; its path must end with '.jinja'.")
        return self
