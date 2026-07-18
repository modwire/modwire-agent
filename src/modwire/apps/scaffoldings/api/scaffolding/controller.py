from typing import Annotated

from ninja import Status
from ninja_extra import route
from wireup import Inject
from wireup.integration.django import inject

from modwire.shared.api.errors import validated
from modwire.shared.api.hypermedia import ResourceController
from modwire.shared.api.types import ShortUUID

from ...services.bundle import ScaffoldingBundleService
from ...services.convergence import ScaffoldingConvergenceService
from ...services.preview import ScaffoldingPreviewService
from ...services.preview_errors import PreviewFailed
from ...services.schema import ScaffoldingSchemaService
from ...services.scaffolding import ScaffoldingService
from .resource import scaffolding
from .schemas import (
    ScaffoldingBundleOut,
    ScaffoldingConvergenceIn,
    ScaffoldingConvergenceOut,
    ScaffoldingFormSchemaOut,
    ScaffoldingPreviewErrorOut,
    ScaffoldingPreviewIn,
    ScaffoldingPreviewOut,
)


@ResourceController(scaffolding)
class ScaffoldingController:
    @route.post(
        "/converge",
        response=ScaffoldingConvergenceOut,
        operation_id="converge_scaffolding",
        summary="Validate or transactionally reconcile a complete scaffolding aggregate.",
    )
    @inject
    def converge(
        self,
        data: ScaffoldingConvergenceIn,
        service: Annotated[ScaffoldingConvergenceService, Inject()],
    ):
        return validated(service.converge, **data.model_dump())

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
