from pydantic import ConfigDict, Field, model_validator

from records.models.content import Content
from shared.api.schema import StrictSchema


class ContentMetadata(StrictSchema):
    """Supported provenance, accessibility, and presentation metadata."""

    source: str = Field(default="", description="Name of the system that supplied the block.")
    source_url: str = Field(default="", description="Canonical URL from which the block was collected.")
    alt: str = Field(default="", description="Accessible alternative text for image content.")
    title: str = Field(default="", description="Optional image title or caption.")


def _content_contract_schema(schema: dict) -> None:
    list_role = Content.Role.LIST.value
    schema["allOf"] = [
        {
            "if": {"properties": {"role": {"const": list_role}}},
            "then": {
                "properties": {
                    "content": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Plain list item strings without presentation markers.",
                    }
                }
            },
            "else": {"properties": {"content": {"type": "string"}}},
        }
    ]


class ContentBlock(StrictSchema):
    """One content object whose role determines its content and rendering semantics."""

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra=_content_contract_schema,
    )

    role: Content.Role = Field(description="Selects the content shape and rendering semantics.")
    content: str | list[str] = Field(
        description="An array of plain strings for lists; a string for every other role.",
        examples=[["First item", "Second item"]],
    )
    language: str = Field(
        min_length=1,
        description="Natural language for prose and lists; syntax identifier for snippets."
    )
    metadata: ContentMetadata = Field(
        default_factory=ContentMetadata,
        description="Typed provenance, accessibility, and presentation metadata.",
    )

    @model_validator(mode="after")
    def validate_role_contract(self):
        if self.role == Content.Role.LIST and not isinstance(self.content, list):
            raise ValueError("List content must be an array of strings.")
        if self.role != Content.Role.LIST and not isinstance(self.content, str):
            raise ValueError("Only list content may be an array.")
        return self
