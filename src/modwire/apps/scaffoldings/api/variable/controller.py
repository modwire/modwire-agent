from modwire.shared.api.hypermedia import ResourceController

from .resource import variable


@ResourceController(variable)
class VariableController:
    pass
