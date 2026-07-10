from ninja import ModelSchema, Schema

from ...models.template import Template


class TemplateIn(Schema):
    scaffolding_id: str
    relative_path: str
    file_content: str


class TemplatePatchIn(Schema):
    relative_path: str
    file_content: str


class TemplateOut(ModelSchema):
    class Meta:
        model = Template 
        fields = "__all__"
