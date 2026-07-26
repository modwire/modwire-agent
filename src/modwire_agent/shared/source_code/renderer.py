import abc
from pathlib import Path

from .package import CodePackage


class CodePackageRenderer(abc.ABC):
    @abc.abstractmethod
    def render(self, root: Path, code_package: CodePackage):
        raise NotImplementedError
