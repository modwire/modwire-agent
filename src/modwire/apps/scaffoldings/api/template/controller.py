from modwire.shared.api.hypermedia import ResourceController

from .resource import template


@ResourceController(template)
class TemplateController:
    pass
