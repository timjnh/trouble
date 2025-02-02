from board import Board
from color import Color

class Game:
    def __init__(self, board: Board):
        self.board = board

    def reset(self):
        self.board.reset()

    @property
    def winner(self) -> Color | None:
        for c in Color:
            if len(self.board.get_pegs_in_final_slots(c)) == 4:
                return c
        return None

    @property
    def is_complete(self) -> bool:
        return self.winner is not None