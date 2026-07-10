from typing import Annotated

from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from ...services.scaffolding import ScaffoldingService
from .schemas import ScaffoldingIn, ScaffoldingOut, ScaffoldingPatchIn


@api_controller("/scaffoldings", tags=["Scaffoldings"])
class ScaffoldingController(ControllerBase):
    @route.get(
        "",
        response=list[ScaffoldingOut],
        operation_id="list_scaffoldings",
        summary="List scaffoldings.",
    )
    @inject
    def list(self, service: Annotated[ScaffoldingService, Inject()]):
        return service.list()

    @route.get(
        "/{scaffolding_id}",
        response=ScaffoldingOut,
        operation_id="get_scaffolding",
        summary="Get scaffolding.",
    )
    @inject
    def get(self, scaffolding_id: int, service: Annotated[ScaffoldingService, Inject()]):
        return service.get(scaffolding_id)

    @route.post(
        "",
        response=ScaffoldingOut,
        operation_id="create_scaffolding",
        summary="Create scaffolding.",
    )
    @inject
    def create(self, data: ScaffoldingIn, service: Annotated[ScaffoldingService, Inject()]):
        return service.create(**data.model_dump())

    @route.put(
        "/{scaffolding_id}",
        response=ScaffoldingOut,
        operation_id="update_scaffolding",
        summary="Update scaffolding.",
    )
    @inject
    def update(
        self,
        scaffolding_id: int,
        data: ScaffoldingIn,
        service: Annotated[ScaffoldingService, Inject()],
    ):
        return service.update(scaffolding_id, **data.model_dump())

    @route.patch(
        "/{scaffolding_id}",
        response=ScaffoldingOut,
        operation_id="partial_update_scaffolding",
        summary="Partially update scaffolding.",
    )
    @inject
    def partial_update(
        self,
        scaffolding_id: int,
        data: ScaffoldingPatchIn,
        service: Annotated[ScaffoldingService, Inject()],
    ):
        return service.update(scaffolding_id, **data.model_dump(exclude_unset=True))

    @route.delete(
        "/{scaffolding_id}",
        response={204: None},
        operation_id="delete_scaffolding",
        summary="Delete scaffolding.",
    )
    @inject
    def delete(self, scaffolding_id: int, service: Annotated[ScaffoldingService, Inject()]):
        service.delete(scaffolding_id)
        return Status(204, None)
