from pydantic import ConfigDict, Field
from pydantic_core import PydanticUndefined

from modwire.apps.records.api.schemas.content import SCHEMA_ROOT, ContentBlock, ContentMetadata
from modwire.apps.records.models.content import Content
from modwire.shared.api.schema import StrictSchema
from modwire.shared.api.types import RecordSlug


class ContentIn(ContentBlock):
    record_slug: RecordSlug
    position: int = Field(ge=0)


class ContentPatchIn(StrictSchema):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "$id": f"{SCHEMA_ROOT}/content-patch-in.schema.json",
            "$schema": "https://json-schema.org/draft/2020-12/schema",
        },
    )

    position: int = Field(default_factory=lambda: PydanticUndefined, ge=0)
    role: Content.Role = Field(
        default_factory=lambda: PydanticUndefined,
        description="Selects the content shape and rendering semantics.",
    )
    content: str | list[str] = Field(
        default_factory=lambda: PydanticUndefined,
        description=(
            "An array of plain strings for lists; a string for every other role. "
            "The persisted result is checked against its effective role."
        ),
    )
    language: str = Field(
        default_factory=lambda: PydanticUndefined,
        description="Natural language for prose and lists; syntax identifier for snippets.",
    )
    metadata: ContentMetadata = Field(
        default_factory=lambda: PydanticUndefined,
        description="Provenance, accessibility, or presentation metadata.",
    )


class ContentOut(ContentBlock):
    id: int
    record_slug: RecordSlug
    position: int

    @staticmethod
    def resolve_record_slug(obj):
        return obj["record_slug"] if isinstance(obj, dict) else obj.record_id
