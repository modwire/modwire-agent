from ninja import Schema
from pydantic import Field
from pydantic_core import PydanticUndefined

from shared.api_schema import StrictSchema
from shared.api_types import Slug


class SectionIn(StrictSchema):
    title: str
    description: str
    tag_slugs: list[Slug]


class SectionPatchIn(StrictSchema):
    title: str = Field(default_factory=lambda: PydanticUndefined)
    description: str = Field(default_factory=lambda: PydanticUndefined)
    tag_slugs: list[Slug] = Field(default_factory=lambda: PydanticUndefined)


class SectionOut(Schema):
    slug: Slug
    title: str
    description: str
    tag_slugs: list[Slug]

    @staticmethod
    def resolve_tag_slugs(obj):
        if isinstance(obj, dict):
            return obj["tag_slugs"]
        return list(obj.tags.order_by("slug").values_list("slug", flat=True))
