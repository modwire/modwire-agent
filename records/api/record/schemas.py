from typing import Literal

from ninja import Schema
from pydantic import Field


class ContentIn(Schema):
    role: Literal["heading", "subheading", "paragraph", "list", "markdown", "snippet", "image"]
    content: str
    language: str
    metadata: dict[str, object] = Field(title="RecordContentInMetadata")


class ContentOut(Schema):
    role: str
    content: str
    language: str
    metadata: dict[str, object] = Field(title="RecordContentOutMetadata")


class RecordIn(Schema):
    section_slug: str
    title: str
    description: str
    sources: list[str]
    tag_slugs: list[str]
    content: list[ContentIn]


class RecordPatchIn(Schema):
    title: str
    description: str
    sources: list[str]
    tag_slugs: list[str]
    content: list[ContentIn]


class RecordOut(Schema):
    slug: str
    local_slug: str
    section_slug: str
    title: str
    description: str
    sources: list[str]
    tag_slugs: list[str]
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
    slug: str
    local_slug: str
    section_slug: str
    title: str
    description: str
    sources: list[str]
    tag_slugs: list[str]

    @staticmethod
    def resolve_section_slug(obj):
        return obj["section_slug"] if isinstance(obj, dict) else obj.section_id

    @staticmethod
    def resolve_tag_slugs(obj):
        if isinstance(obj, dict):
            return obj["tag_slugs"]
        return list(obj.tags.order_by("slug").values_list("slug", flat=True))


class SearchIn(Schema):
    query: str
    mode: Literal["fts", "vector"]
    target: Literal["records", "sections", "all"]
    limit: int = Field(ge=1, le=100)
    offset: int = Field(ge=0)
    section_slugs: list[str]
    tag_slugs: list[str]


class RecordSearchResultOut(Schema):
    kind: Literal["record"]
    slug: str
    score: float
    title: str
    section_slug: str


class SectionSearchResultOut(Schema):
    kind: Literal["section"]
    slug: str
    score: float
    title: str


class SearchOut(Schema):
    results: list[RecordSearchResultOut | SectionSearchResultOut]
