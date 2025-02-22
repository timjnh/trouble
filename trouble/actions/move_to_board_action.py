from .action import Action
from .. import Color, Board

class MoveToBoardAction(Action):
    def __init__(self, die_roll: int, color: Color, board: Board):
        self.die_roll = die_roll
        self.color = color
        self.board = board

    def is_applicable(self) -> bool:
        if self.die_roll != 6:
            return False
        
        board_start_position = self.board.track_position_to_board_position(0, self.color)
        assert board_start_position is not None
        peg_at_starting_position = self.board.get_peg_at_board_position(board_start_position)

        if peg_at_starting_position is not None and peg_at_starting_position.color == self.color:
            return False

        on_deck_pegs = self.board.get_pegs_on_deck(self.color)
        if len(on_deck_pegs) == 0:
            return False
        return True

    def apply(self):
        peg = self.board.get_pegs_on_deck(self.color)[0]

        # bounce any pegs at our start position to on deck
        board_peg_position = self.board.track_position_to_board_position(0, peg.color)
        assert board_peg_position is not None
        other_peg = self.board.get_peg_at_board_position(board_peg_position)
        if other_peg is not None:
            self.board.set_peg_on_deck(other_peg)

        # move us onto the board
        self.board.set_peg_track_position(peg, 0)