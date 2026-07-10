from ninja import ModelSchema, Schema

from ...models.scaffolding import Scaffolding


class ScaffoldingIn(Schema):
    language_id: str
    name: str
    description: str


class ScaffoldingPatchIn(Schema):
    language_id: str | None = None
    name: str | None = None
    description: str | None = None


class ScaffoldingOut(ModelSchema):
    class Meta:
        model = Scaffolding 
        fields = "__all__"
