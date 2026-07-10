from typing import Annotated

from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from shared.api_errors import validated

from ...services.package_manager import PackageManagerService
from .schemas import PackageManagerIn, PackageManagerOut, PackageManagerPatchIn


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

    @route.get(
        "/{package_manager_id}",
        response=PackageManagerOut,
        operation_id="get_package_manager",
        summary="Get package_manager.",
    )
    @inject
    def get(self, package_manager_id: str, service: Annotated[PackageManagerService, Inject()]):
        return service.get(package_manager_id)

    @route.post(
        "",
        response=PackageManagerOut,
        operation_id="create_package_manager",
        summary="Create package_manager.",
    )
    @inject
    def create(self, data: PackageManagerIn, service: Annotated[PackageManagerService, Inject()]):
        return validated(service.create, **data.model_dump())

    @route.put(
        "/{package_manager_id}",
        response=PackageManagerOut,
        operation_id="update_package_manager",
        summary="Update package_manager.",
    )
    @inject
    def update(
        self,
        package_manager_id: str,
        data: PackageManagerIn,
        service: Annotated[PackageManagerService, Inject()],
    ):
        return validated(service.update, package_manager_id, **data.model_dump())

    @route.patch(
        "/{package_manager_id}",
        response=PackageManagerOut,
        operation_id="partial_update_package_manager",
        summary="Partially update package_manager.",
    )
    @inject
    def partial_update(
        self,
        package_manager_id: str,
        data: PackageManagerPatchIn,
        service: Annotated[PackageManagerService, Inject()],
    ):
        return validated(service.update, package_manager_id, **data.model_dump(exclude_unset=True))

    @route.delete(
        "/{package_manager_id}",
        response={204: None},
        operation_id="delete_package_manager",
        summary="Delete package_manager.",
    )
    @inject
    def delete(self, package_manager_id: str, service: Annotated[PackageManagerService, Inject()]):
        service.delete(package_manager_id)
        return Status(204, None)
