import abc
from collections.abc import Mapping

from .errors import SourceCodeError
from .package import SourceCodePackage


class SourceCodeRenderer(abc.ABC):
    @abc.abstractmethod
    def render(
        self,
        source: SourceCodePackage,
        data: Mapping[str, object],
    ) -> SourceCodePackage:
        raise SourceCodeError("Source code rendering is not implemented.")
