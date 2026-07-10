from ninja import ModelSchema, Schema

from ...models.template import Template 


class TemplateIn(Schema):
    name: str


class TemplatePatchIn(Schema):
    name: str


class TemplateOut(ModelSchema):
    class Meta:
        model = Template 
        fields = ("id", "name", "created_at", "updated_at")
