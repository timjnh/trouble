from abc import ABC, abstractmethod

class Die(ABC):
    def __init__(self, sides: int = 6):
        self.sides = sides

    @abstractmethod
    def roll(self) -> int:
        pass