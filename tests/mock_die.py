from typing import List

from trouble.die import Die

class MockDie(Die):
    def __init__(self, rolls: List[int], sides: int | None = None):
        if sides is not None:
            super().__init__(sides)
        else:
            super().__init__()

        self.rolls = rolls
        self._position = 0

    def roll(self) -> int:
        roll = self.rolls[self._position]
        if self._position < len(self.rolls) - 1:
            self._position += 1
        return roll