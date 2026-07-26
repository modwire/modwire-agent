from abc import ABC, abstractmethod


class PlansInbound(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError
