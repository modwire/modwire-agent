from modwire.apps.scaffoldings.services.template import TemplateService
from modwire.shared.api.errors import validation_error
from modwire.shared.api.hypermedia import CrudResource, ResourceSpec
from modwire.shared.api.types import ShortUUID

from .schemas import TemplateIn, TemplateOut, TemplatePatchIn

template = CrudResource(
    name="template",
    collection_path="/api/templates",
    entity_path="/api/templates/{template_id}",
    path_parameter="template_id",
    path_parameter_type=ShortUUID,
    in_schema=TemplateIn,
    out_schema=TemplateOut,
    patch_schema=TemplatePatchIn,
    service=TemplateService,
    tags=("Templates",),
    summaries={
        "list": "List templates.",
        "get": "Get template.",
        "create": "Create template.",
        "update": "Update template.",
        "partial_update": "Partially update template.",
        "delete": "Delete template.",
    },
    validation_error=validation_error,
)

SIREN_RESOURCES = (
    ResourceSpec(
        name="template",
        path="/api/templates/{template_id}",
        resource_class="template",
        identifier="id",
        path_parameters={"template_id": "id"},
        relations={"scaffolding": {"rel": "scaffolding", "resource": "scaffolding", "many": False}},
    ),
)
