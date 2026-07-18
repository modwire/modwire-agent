from modwire.shared.api.hypermedia import ResourceController

from .resource import section


@ResourceController(section)
class SectionController:
    pass
