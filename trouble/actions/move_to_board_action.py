from .action import Action
from .. import Peg, Board

class MoveToBoardAction(Action):
    def __init__(self, peg: Peg, board: Board):
        self.peg = peg
        self.board = board

    def apply(self):
        assert self.board.is_peg_on_deck(self.peg)

        # bounce any pegs at our start position to on deck
        board_peg_position = self.board.track_position_to_board_position(0, self.peg.color)
        other_peg = self.board.get_peg_at_board_position(board_peg_position)
        if other_peg is not None:
            self.board.set_peg_on_deck(other_peg)

        # move us onto the board
        self.board.set_peg_track_position(self.peg, 0)