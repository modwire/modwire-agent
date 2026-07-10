from ninja import ModelSchema

from ...models.tool import Tool


class ToolOut(ModelSchema):
    class Meta:
        model = Tool
        fields = "__all__"
