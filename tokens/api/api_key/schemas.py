from ninja import ModelSchema, Schema

from ...models.api_key import ApiKey


class ApiKeyIn(Schema):
    name: str


class ApiKeyPatchIn(Schema):
    name: str


class ApiKeyOut(ModelSchema):
    class Meta:
        model = ApiKey
        fields = ("id", "name", "created_at", "updated_at")
