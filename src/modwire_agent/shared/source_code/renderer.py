import abc
from collections.abc import Mapping
from pathlib import Path

from .code_map import SourceCodeMap
from .package import SourceCodePackage


class SourceCodeRenderer(abc.ABC):
    @abc.abstractmethod
    def render(
        self,
        root: Path,
        source: SourceCodePackage,
        data: Mapping[str, object],
    ) -> SourceCodeMap:
        raise NotImplementedError
