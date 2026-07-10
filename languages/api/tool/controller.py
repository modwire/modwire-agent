from typing import Annotated

from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from ...services.tool import ToolService
from .schemas import ToolOut


@api_controller("/tools", tags=["Tools"])
class ToolController(ControllerBase):
    @route.get(
        "",
        response=list[ToolOut],
        operation_id="list_tools",
        summary="List tools.",
    )
    @inject
    def list(
        self,
        language_id: str,
        role: str,
        service: Annotated[ToolService, Inject()],
    ):
        return service.list(language_id=language_id, role=role)
