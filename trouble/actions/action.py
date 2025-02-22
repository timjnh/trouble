from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def is_applicable(self) -> bool:
        pass

    @abstractmethod
    def apply(self):
        pass