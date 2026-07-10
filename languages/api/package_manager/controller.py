from typing import Annotated

from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from ...services.package_manager import PackageManagerService
from .schemas import PackageManagerOut


@api_controller("/package_managers", tags=["PackageManagers"])
class PackageManagerController(ControllerBase):
    @route.get(
        "",
        response=list[PackageManagerOut],
        operation_id="list_package_managers",
        summary="List package_managers.",
    )
    @inject
    def list(self, service: Annotated[PackageManagerService, Inject()]):
        return service.list()
