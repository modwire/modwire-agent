from typing import Annotated

from ninja import Status
from ninja_extra import ControllerBase, api_controller, route
from wireup import Inject
from wireup.integration.django import inject

from ...services.template import TemplateService
from .schemas import TemplateIn, TemplateOut, TemplatePatchIn


@api_controller("/templates", tags=["Templates"])
class TemplateController(ControllerBase):
    @route.get(
        "",
        response=list[TemplateOut],
        operation_id="list_templates",
        summary="List templates.",
    )
    @inject
    def list(self, service: Annotated[TemplateService, Inject()]):
        return service.list()

    @route.get(
        "/{template_id}",
        response=TemplateOut,
        operation_id="get_template",
        summary="Get template.",
    )
    @inject
    def get(self, template_id: int, service: Annotated[TemplateService, Inject()]):
        return service.get(template_id)

    @route.post(
        "",
        response=TemplateOut,
        operation_id="create_template",
        summary="Create template.",
    )
    @inject
    def create(self, data: TemplateIn, service: Annotated[TemplateService, Inject()]):
        return service.create(**data.model_dump())

    @route.put(
        "/{template_id}",
        response=TemplateOut,
        operation_id="update_template",
        summary="Update template.",
    )
    @inject
    def update(
        self,
        template_id: int,
        data: TemplateIn,
        service: Annotated[TemplateService, Inject()],
    ):
        return service.update(template_id, **data.model_dump())

    @route.patch(
        "/{template_id}",
        response=TemplateOut,
        operation_id="partial_update_template",
        summary="Partially update template.",
    )
    @inject
    def partial_update(
        self,
        template_id: int,
        data: TemplatePatchIn,
        service: Annotated[TemplateService, Inject()],
    ):
        return service.update(template_id, **data.model_dump(exclude_unset=True))

    @route.delete(
        "/{template_id}",
        response={204: None},
        operation_id="delete_template",
        summary="Delete template.",
    )
    @inject
    def delete(self, template_id: int, service: Annotated[TemplateService, Inject()]):
        service.delete(template_id)
        return Status(204, None)
