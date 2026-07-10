from ninja import Field, ModelSchema
from pydantic_core import PydanticUndefined

from shared.api.schema import StrictSchema

from ...models.api_key import ApiKey


class ApiKeyIn(StrictSchema):
    name: str


class ApiKeyPatchIn(StrictSchema):
    name: str = Field(default_factory=lambda: PydanticUndefined)


class ApiKeyOut(ModelSchema):
    id: int

    class Meta:
        model = ApiKey
        fields = ("id", "name", "created_at", "updated_at")


class ApiKeyCreatedOut(ApiKeyOut):
    key: str
