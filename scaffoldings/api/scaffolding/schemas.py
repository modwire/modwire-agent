from ninja import ModelSchema, Schema

from ...models.scaffolding import Scaffolding 


class ScaffoldingIn(Schema):
    name: str


class ScaffoldingPatchIn(Schema):
    name: str


class ScaffoldingOut(ModelSchema):
    class Meta:
        model = Scaffolding 
        fields = ("id", "name", "created_at", "updated_at")
