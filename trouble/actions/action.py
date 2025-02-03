from abc import ABC, abstractmethod

class Action(ABC):
    @abstractmethod
    def apply(self):
        pass