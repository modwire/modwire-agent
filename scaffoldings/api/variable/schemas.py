from ninja import Field, ModelSchema
from pydantic import JsonValue
from pydantic_core import PydanticUndefined

from shared.api.schema import StrictSchema
from shared.api.types import ShortUUID

from ...models.variable import Variable, VariableType


class VariableIn(StrictSchema):
    scaffolding_id: ShortUUID
    name: str
    type: VariableType
    description: str
    default_value: JsonValue
    required: bool = False


class VariablePatchIn(StrictSchema):
    name: str = Field(default_factory=lambda: PydanticUndefined)
    type: VariableType = Field(default_factory=lambda: PydanticUndefined)
    description: str = Field(default_factory=lambda: PydanticUndefined)
    default_value: JsonValue = Field(default_factory=lambda: PydanticUndefined)
    required: bool = Field(default_factory=lambda: PydanticUndefined)


class VariableOut(ModelSchema):
    id: ShortUUID
    scaffolding: ShortUUID
    type: VariableType
    default_value: JsonValue

    @staticmethod
    def resolve_scaffolding(obj):
        return obj.scaffolding_id

    class Meta:
        model = Variable 
        fields = "__all__"
