from abc import ABC, abstractmethod

from .operation_handler import OperationHandler


class OperationCatalog(ABC):
    @abstractmethod
    def resolve(self, extension_key: str, extension_version: int) -> OperationHandler:
        raise NotImplementedError
