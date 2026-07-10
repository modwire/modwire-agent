from typing import Any

from ninja import ModelSchema, Schema

from ...models.variable import Variable


class VariableIn(Schema):
    scaffolding_id: str
    name: str
    type: str
    description: str
    default_value: Any


class VariablePatchIn(Schema):
    scaffolding_id: str | None = None
    name: str | None = None
    type: str | None = None
    description: str | None = None
    default_value: Any | None = None


class VariableOut(ModelSchema):
    class Meta:
        model = Variable 
        fields = "__all__"
