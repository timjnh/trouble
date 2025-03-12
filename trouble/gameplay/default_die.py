import random

from .die import Die

class DefaultDie(Die):
    def __init__(self):
        super().__init__()
        self.last_roll = None

    def roll(self) -> int:
        self.last_roll = random.randint(1, self.sides)
        return self.last_roll