import random

from .die import Die

class DefaultDie(Die):
    def roll(self) -> int:
        return random.randint(1, self.sides)