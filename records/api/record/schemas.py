from typing import Literal

from ninja import Schema
from pydantic import Field, JsonValue
from pydantic_core import PydanticUndefined

from shared.api.schema import StrictSchema
from shared.api.types import RecordSlug, Slug


class ContentIn(StrictSchema):
    role: Literal["heading", "subheading", "paragraph", "list", "markdown", "snippet", "image"]
    content: str
    language: str
    metadata: dict[str, JsonValue] = Field(title="RecordContentInMetadata")


class ContentOut(Schema):
    role: Literal["heading", "subheading", "paragraph", "list", "markdown", "snippet", "image"]
    content: str
    language: str
    metadata: dict[str, JsonValue] = Field(title="RecordContentOutMetadata")


class RecordIn(StrictSchema):
    section_slug: Slug
    title: str
    description: str
    sources: list[str]
    tag_slugs: list[Slug]
    content: list[ContentIn]


class RecordPatchIn(StrictSchema):
    title: str = Field(default_factory=lambda: PydanticUndefined)
    description: str = Field(default_factory=lambda: PydanticUndefined)
    sources: list[str] = Field(default_factory=lambda: PydanticUndefined)
    tag_slugs: list[Slug] = Field(default_factory=lambda: PydanticUndefined)
    content: list[ContentIn] = Field(default_factory=lambda: PydanticUndefined)


class RecordOut(Schema):
    slug: RecordSlug
    local_slug: Slug
    section_slug: Slug
    title: str
    description: str
    sources: list[str]
    tag_slugs: list[Slug]
    content: list[ContentOut]

    @staticmethod
    def resolve_section_slug(obj):
        if isinstance(obj, dict):
            return obj["section_slug"]
        return obj.section_id

    @staticmethod
    def resolve_tag_slugs(obj):
        if isinstance(obj, dict):
            return obj["tag_slugs"]
        return list(obj.tags.order_by("slug").values_list("slug", flat=True))

    @staticmethod
    def resolve_content(obj):
        if isinstance(obj, dict):
            return obj["content"]
        return [
            {
                "role": item.role,
                "content": item.content,
                "language": item.language,
                "metadata": item.metadata,
            }
            for item in obj.content.order_by("position", "id")
        ]


class RecordSummaryOut(Schema):
    slug: RecordSlug
    local_slug: Slug
    section_slug: Slug
    title: str
    description: str
    sources: list[str]
    tag_slugs: list[Slug]

    @staticmethod
    def resolve_section_slug(obj):
        return obj["section_slug"] if isinstance(obj, dict) else obj.section_id

    @staticmethod
    def resolve_tag_slugs(obj):
        if isinstance(obj, dict):
            return obj["tag_slugs"]
        return list(obj.tags.order_by("slug").values_list("slug", flat=True))


class SearchIn(StrictSchema):
    query: str
    mode: Literal["fts", "vector"]
    target: Literal["records", "sections", "all"]
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)
    section_slugs: list[Slug]
    tag_slugs: list[Slug]


class RecordSearchResultOut(Schema):
    kind: Literal["record"]
    slug: RecordSlug
    score: float
    title: str
    section_slug: Slug


class SectionSearchResultOut(Schema):
    kind: Literal["section"]
    slug: Slug
    score: float
    title: str


class SearchOut(Schema):
    results: list[RecordSearchResultOut | SectionSearchResultOut]
