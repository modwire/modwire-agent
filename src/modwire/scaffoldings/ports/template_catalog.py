from abc import ABC, abstractmethod
from typing import Any


class TemplateCatalog(ABC):
    @abstractmethod
    def get(self, identifier: str) -> Any:
        raise NotImplementedError
