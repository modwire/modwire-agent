from ninja import ModelSchema, Schema

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
