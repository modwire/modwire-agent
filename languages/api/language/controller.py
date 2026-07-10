from typing import Annotated

from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from ...services.language import LanguageService
from .schemas import LanguageOut


@api_controller("/languages", tags=["Languages"])
class LanguageController(ControllerBase):
    @route.get(
        "",
        response=list[LanguageOut],
        operation_id="list_languages",
        summary="List languages.",
    )
    @inject
    def list(self, service: Annotated[LanguageService, Inject()]):
        return service.list()
