import abc
from collections.abc import Mapping

from .package import SourceCodePackage


class SourceCodeRenderer(abc.ABC):
    @abc.abstractmethod
    def render(
        self,
        source: SourceCodePackage,
        data: Mapping[str, object],
    ) -> SourceCodePackage:
        raise NotImplementedError
