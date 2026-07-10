from typing import Annotated

from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from shared.api_types import ShortUUID

from ...services.command import CommandService
from .schemas import CommandOut


@api_controller("/commands", tags=["Commands"])
class CommandController(ControllerBase):
    @route.get(
        "",
        response=list[CommandOut],
        operation_id="list_commands",
        summary="List commands.",
    )
    @inject
    def list(self, package_manager_id: ShortUUID, service: Annotated[CommandService, Inject()]):
        return service.list(package_manager_id=package_manager_id)
