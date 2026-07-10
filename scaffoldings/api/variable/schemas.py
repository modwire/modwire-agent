from ninja import ModelSchema, Schema

from ...models.variable import Variable 


class VariableIn(Schema):
    name: str


class VariablePatchIn(Schema):
    name: str


class VariableOut(ModelSchema):
    class Meta:
        model = Variable 
        fields = "__all__"
