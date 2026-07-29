from ..shared import DomainError


class ScaffoldingError(DomainError): ...


class ScaffoldingRenderingFailed(ScaffoldingError): ...
