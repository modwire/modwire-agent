from typing import Literal

from ninja import Schema
from pydantic import Field

from modwire.shared.api.schema import StrictSchema


class SearchIn(StrictSchema):
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
