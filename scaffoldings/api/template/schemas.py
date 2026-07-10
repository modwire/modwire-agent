from ninja import ModelSchema, Schema

from ...models.template import Template


class TemplateIn(Schema):
    scaffolding_id: str
    relative_path: str
    file_content: str


class TemplatePatchIn(Schema):
    scaffolding_id: str | None = None
    relative_path: str | None = None
    file_content: str | None = None


class TemplateOut(ModelSchema):
    class Meta:
        model = Template 
        fields = "__all__"
