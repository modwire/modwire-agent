from ninja import Schema
from pydantic import Field
from pydantic_core import PydanticUndefined

from shared.api_schema import StrictSchema
from shared.api_types import Slug


class TagIn(StrictSchema):
    name: str
    description: str


class TagPatchIn(StrictSchema):
    name: str = Field(default_factory=lambda: PydanticUndefined)
    description: str = Field(default_factory=lambda: PydanticUndefined)


class TagOut(Schema):
    slug: Slug
    name: str
    description: str

    @staticmethod
    def resolve_slug(obj):
        return obj["slug"] if isinstance(obj, dict) else obj.slug
