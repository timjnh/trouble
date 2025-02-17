from .action import Action
from .. import Peg, Board

class MoveToBoardAction(Action):
    def __init__(self, peg: Peg, board: Board):
        self.peg = peg
        self.board = board

    def apply(self):
        assert self.peg.is_on_deck

        # bounce any pegs at our start position to on deck
        board_peg_position = self.board.track_position_to_board_position(0, self.peg.color)
        other_peg = self.board.get_peg_at_board_position(board_peg_position)
        if other_peg is not None:
            other_peg.move_to_on_deck()

        # move us onto the board
        self.peg.position = 0