from typing import Annotated

from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from shared.api_types import ShortUUID

from ...services.tool_command import ToolCommandService
from .schemas import ToolCommandOut


@api_controller("/tool_commands", tags=["ToolCommands"])
class ToolCommandController(ControllerBase):
    @route.get(
        "",
        response=list[ToolCommandOut],
        operation_id="list_tool_commands",
        summary="List tool_commands.",
    )
    @inject
    def list(self, tool_id: ShortUUID, service: Annotated[ToolCommandService, Inject()]):
        return service.list(tool_id=tool_id)
