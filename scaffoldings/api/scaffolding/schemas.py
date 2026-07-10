from typing import Any

from ninja import Field, ModelSchema, Schema

from ...models.scaffolding import Scaffolding


class ScaffoldingIn(Schema):
    language_id: str
    name: str
    description: str


class ScaffoldingPatchIn(Schema):
    name: str
    description: str


class ScaffoldingOut(ModelSchema):
    class Meta:
        model = Scaffolding 
        fields = "__all__"


class TemplateOverrideIn(Schema):
    template_id: str
    relative_path: str
    file_content: str


class ScaffoldingPreviewIn(Schema):
    values: dict[str, Any] = Field(default_factory=dict)
    template_overrides: list[TemplateOverrideIn] = Field(default_factory=list)


class PreviewFileOut(Schema):
    template_id: str
    path: str
    source: str
    html: str
    language: str


class ScaffoldingPreviewOut(Schema):
    files: list[PreviewFileOut]


class PreviewErrorOut(Schema):
    code: str
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class ScaffoldingPreviewErrorOut(Schema):
    errors: list[PreviewErrorOut]
