from abc import ABC, abstractmethod

from ...domain.run.stage_transition import StageTransition


class StageTransitionStore(ABC):
    @abstractmethod
    def commit(self, transition: StageTransition) -> None:
        raise NotImplementedError
