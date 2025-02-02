from .color import Color

class Peg:
    def __init__(self, color: Color):
        self.color = color
        self._position: int | None = None # represents the position of the peg on its own track (including the four final slots)

    def reset(self):
        self._position = None

    @property
    def position(self) -> int | None:
        return self._position

    @position.setter
    def position(self, position: int):
        self._position = position

    @property
    def is_on_board(self) -> bool:
        return self._position != None
    
    @property
    def is_on_deck(self) -> bool:
        return not self.is_on_board