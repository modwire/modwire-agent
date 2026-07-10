from typing import Annotated

from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from shared.api.errors import validated
from shared.api.types import ShortUUID

from ...services.bundle import ScaffoldingBundleService
from ...services.preview import ScaffoldingPreviewService
from ...services.preview_errors import PreviewFailed
from ...services.scaffolding import ScaffoldingService
from ...services.schema import ScaffoldingSchemaService
from .schemas import (
    ScaffoldingBundleOut,
    ScaffoldingFormSchemaOut,
    ScaffoldingIn,
    ScaffoldingOut,
    ScaffoldingPatchIn,
    ScaffoldingPreviewErrorOut,
    ScaffoldingPreviewIn,
    ScaffoldingPreviewOut,
)


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
    def get(self, scaffolding_id: ShortUUID, service: Annotated[ScaffoldingService, Inject()]):
        return service.get(scaffolding_id)

    @route.get(
        "/{scaffolding_id}/schema",
        response=ScaffoldingFormSchemaOut,
        by_alias=True,
        operation_id="get_scaffolding_schema",
        summary="Get the scaffolding variable form schema.",
    )
    @inject
    def schema(
        self,
        scaffolding_id: ShortUUID,
        scaffoldings: Annotated[ScaffoldingService, Inject()],
        schemas: Annotated[ScaffoldingSchemaService, Inject()],
    ):
        return schemas.build(scaffoldings.get(scaffolding_id))

    @route.get(
        "/{scaffolding_id}/bundle",
        response=ScaffoldingBundleOut,
        operation_id="get_scaffolding_bundle",
        summary="Get a generic scaffolding bundle for a local generator.",
    )
    @inject
    def bundle(self, scaffolding_id: ShortUUID, service: Annotated[ScaffoldingBundleService, Inject()]):
        return service.get(scaffolding_id)

    @route.post(
        "/{scaffolding_id}/preview",
        response={200: ScaffoldingPreviewOut, 422: ScaffoldingPreviewErrorOut},
        operation_id="preview_scaffolding",
        summary="Preview a rendered scaffolding.",
    )
    @inject
    def preview(
        self,
        scaffolding_id: ShortUUID,
        data: ScaffoldingPreviewIn,
        service: Annotated[ScaffoldingPreviewService, Inject()],
    ):
        try:
            return service.preview(
                scaffolding_id,
                data.values,
                [override.model_dump(exclude_none=True) for override in data.template_overrides],
            )
        except PreviewFailed as error:
            return Status(422, {"errors": [item.as_dict() for item in error.errors]})

    @route.post(
        "",
        response=ScaffoldingOut,
        operation_id="create_scaffolding",
        summary="Create scaffolding.",
    )
    @inject
    def create(self, data: ScaffoldingIn, service: Annotated[ScaffoldingService, Inject()]):
        return validated(service.create, **data.model_dump())

    @route.put(
        "/{scaffolding_id}",
        response=ScaffoldingOut,
        operation_id="update_scaffolding",
        summary="Update scaffolding.",
    )
    @inject
    def update(
        self,
        scaffolding_id: ShortUUID,
        data: ScaffoldingIn,
        service: Annotated[ScaffoldingService, Inject()],
    ):
        return validated(service.update, scaffolding_id, **data.model_dump())

    @route.patch(
        "/{scaffolding_id}",
        response=ScaffoldingOut,
        operation_id="partial_update_scaffolding",
        summary="Partially update scaffolding.",
    )
    @inject
    def partial_update(
        self,
        scaffolding_id: ShortUUID,
        data: ScaffoldingPatchIn,
        service: Annotated[ScaffoldingService, Inject()],
    ):
        return validated(service.update, scaffolding_id, **data.model_dump(exclude_unset=True, warnings=False))

    @route.delete(
        "/{scaffolding_id}",
        response={204: None},
        operation_id="delete_scaffolding",
        summary="Delete scaffolding.",
    )
    @inject
    def delete(self, scaffolding_id: ShortUUID, service: Annotated[ScaffoldingService, Inject()]):
        service.delete(scaffolding_id)
        return Status(204, None)
