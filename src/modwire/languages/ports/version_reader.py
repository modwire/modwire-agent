from abc import ABC, abstractmethod

from ..domain.contracts import Language


class VersionReader(ABC):
    @abstractmethod
    def read(self, language: Language, timeout: float) -> str:
        raise NotImplementedError
