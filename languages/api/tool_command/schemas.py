from ninja import ModelSchema

from shared.api.types import ShortUUID

from ...models.tool_command import ToolCommand, ToolCommandCapability


class ToolCommandOut(ModelSchema):
    id: ShortUUID
    tool: ShortUUID
    capability: ToolCommandCapability

    @staticmethod
    def resolve_tool(obj):
        return obj.tool_id

    class Meta:
        model = ToolCommand
        fields = "__all__"
