from typing import Any

from ninja import ModelSchema, Schema

from ...models.variable import Variable


class VariableIn(Schema):
    scaffolding_id: str
    name: str
    type: str
    description: str
    default_value: Any
    required: bool = False


class VariablePatchIn(Schema):
    name: str
    type: str
    description: str
    default_value: Any
    required: bool


class VariableOut(ModelSchema):
    class Meta:
        model = Variable 
        fields = "__all__"
