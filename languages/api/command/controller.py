from typing import Annotated

from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from shared.api_errors import validated

from ...services.command import CommandService
from .schemas import CommandIn, CommandOut, CommandPatchIn


@api_controller("/commands", tags=["Commands"])
class CommandController(ControllerBase):
    @route.get(
        "",
        response=list[CommandOut],
        operation_id="list_commands",
        summary="List commands.",
    )
    @inject
    def list(self, service: Annotated[CommandService, Inject()]):
        return service.list()

    @route.get(
        "/{command_id}",
        response=CommandOut,
        operation_id="get_command",
        summary="Get command.",
    )
    @inject
    def get(self, command_id: str, service: Annotated[CommandService, Inject()]):
        return service.get(command_id)

    @route.post(
        "",
        response=CommandOut,
        operation_id="create_command",
        summary="Create command.",
    )
    @inject
    def create(self, data: CommandIn, service: Annotated[CommandService, Inject()]):
        return validated(service.create, **data.model_dump())

    @route.put(
        "/{command_id}",
        response=CommandOut,
        operation_id="update_command",
        summary="Update command.",
    )
    @inject
    def update(
        self,
        command_id: str,
        data: CommandIn,
        service: Annotated[CommandService, Inject()],
    ):
        return validated(service.update, command_id, **data.model_dump())

    @route.patch(
        "/{command_id}",
        response=CommandOut,
        operation_id="partial_update_command",
        summary="Partially update command.",
    )
    @inject
    def partial_update(
        self,
        command_id: str,
        data: CommandPatchIn,
        service: Annotated[CommandService, Inject()],
    ):
        return validated(service.update, command_id, **data.model_dump(exclude_unset=True))

    @route.delete(
        "/{command_id}",
        response={204: None},
        operation_id="delete_command",
        summary="Delete command.",
    )
    @inject
    def delete(self, command_id: str, service: Annotated[CommandService, Inject()]):
        service.delete(command_id)
        return Status(204, None)
