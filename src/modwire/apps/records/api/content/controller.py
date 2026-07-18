from modwire.shared.api.hypermedia import ResourceController

from .resource import content


@ResourceController(content)
class ContentController:
    pass
