from typing import Literal

from ninja import Schema
from pydantic import Field, JsonValue
from pydantic_core import PydanticUndefined

from shared.api.schema import StrictSchema
from shared.api.types import RecordSlug

type ContentRole = Literal[
    "heading",
    "subheading",
    "paragraph",
    "list",
    "markdown",
    "snippet",
    "image",
]


class ContentIn(StrictSchema):
    record_slug: RecordSlug
    position: int = Field(ge=0)
    role: ContentRole
    content: str
    language: str
    metadata: dict[str, JsonValue] = Field(title="ContentInMetadata")


class ContentPatchIn(StrictSchema):
    position: int = Field(default_factory=lambda: PydanticUndefined, ge=0)
    role: ContentRole = Field(default_factory=lambda: PydanticUndefined)
    content: str = Field(default_factory=lambda: PydanticUndefined)
    language: str = Field(default_factory=lambda: PydanticUndefined)
    metadata: dict[str, JsonValue] = Field(default_factory=lambda: PydanticUndefined)


class ContentOut(Schema):
    id: int
    record_slug: RecordSlug
    position: int
    role: ContentRole
    content: str
    language: str
    metadata: dict[str, JsonValue] = Field(title="ContentOutMetadata")

    @staticmethod
    def resolve_record_slug(obj):
        return obj["record_slug"] if isinstance(obj, dict) else obj.record_id
