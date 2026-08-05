from ninja import Schema
from pydantic import Field, JsonValue


class CategoryInput(Schema):
    title: str
    content_schema: dict[str, JsonValue]


class Category(Schema):
    id: str
    title: str
    content_schema: dict[str, JsonValue]


class TagInput(Schema):
    name: str


class Tag(Schema):
    id: str
    name: str


class ResourceInput(Schema):
    path: str
    language: str
    content: str


class Resource(Schema):
    path: str
    language: str
    content: str


class RecordInput(Schema):
    title: str
    content: dict[str, JsonValue]
    category_id: str
    tag_ids: list[str] = Field(min_length=1)
    resources: list[ResourceInput] = Field(default_factory=list)


class RecordSummary(Schema):
    id: str
    title: str
    category: Category
    tags: list[Tag]


class Record(RecordSummary):
    content: dict[str, JsonValue]
    resources: list[Resource]


class SearchInput(Schema):
    query: str = Field(min_length=1, pattern=r"\S")
    limit: int = Field(default=10, ge=1)
