from modwire.shared.api.hypermedia import ResourceController

from .resource import tag


@ResourceController(tag)
class TagController:
    pass
