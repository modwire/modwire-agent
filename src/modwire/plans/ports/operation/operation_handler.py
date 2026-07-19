from abc import ABC, abstractmethod

from ...domain.operation.operation_context import OperationContext


class OperationHandler(ABC):
    @abstractmethod
    def key(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def version(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def require_valid_configuration(self, configuration: dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(self, context: OperationContext) -> dict:
        raise NotImplementedError
