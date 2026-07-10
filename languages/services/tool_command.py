from wireup import injectable

from ..models.tool_command import ToolCommand


@injectable
class ToolCommandService:
    model = ToolCommand

    def list(self, tool_id: str):
        queryset = self.model.objects.select_related("tool").order_by("tool", "capability")
        return queryset.filter(tool_id=tool_id)

    def upsert(self, *, tool, capability: str, cmd: str):
        instance, _ = self.model.objects.update_or_create(
            tool=tool,
            capability=capability,
            defaults={"cmd": cmd},
        )
        return instance
