from ninja import Field, ModelSchema
from pydantic_core import PydanticUndefined

from modwire.shared.api.schema import StrictSchema
from modwire.shared.api.types import ShortUUID

from ...models.template import Template


class TemplateIn(StrictSchema):
    scaffolding_id: ShortUUID
    relative_path: str
    file_content: str
    write_mode: Template.WriteMode = Template.WriteMode.MANAGED


class TemplatePatchIn(StrictSchema):
    relative_path: str = Field(default_factory=lambda: PydanticUndefined)
    file_content: str = Field(default_factory=lambda: PydanticUndefined)
    write_mode: Template.WriteMode = Field(default_factory=lambda: PydanticUndefined)


class TemplateOut(ModelSchema):
    id: ShortUUID
    scaffolding: ShortUUID
    file_content: str

    @staticmethod
    def resolve_scaffolding(obj):
        return obj.scaffolding_id

    class Meta:
        model = Template
        fields = "__all__"
