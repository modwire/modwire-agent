from ninja import ModelSchema

from ...models.tool_command import ToolCommand


class ToolCommandOut(ModelSchema):
    class Meta:
        model = ToolCommand
        fields = "__all__"
