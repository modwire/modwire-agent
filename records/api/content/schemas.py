from typing import Literal

from ninja import Schema
from pydantic import Field

type ContentRole = Literal[
    "heading",
    "subheading",
    "paragraph",
    "list",
    "markdown",
    "snippet",
    "image",
]


class ContentIn(Schema):
    record_slug: str
    position: int = Field(ge=0)
    role: ContentRole
    content: str
    language: str
    metadata: dict[str, object] = Field(title="ContentInMetadata")


class ContentPatchIn(Schema):
    position: int = Field(ge=0)
    role: ContentRole
    content: str
    language: str
    metadata: dict[str, object] = Field(title="ContentPatchInMetadata")


class ContentOut(Schema):
    id: int
    record_slug: str
    position: int
    role: str
    content: str
    language: str
    metadata: dict[str, object] = Field(title="ContentOutMetadata")

    @staticmethod
    def resolve_record_slug(obj):
        return obj["record_slug"] if isinstance(obj, dict) else obj.record_id
