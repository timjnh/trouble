from typing import List

from .action import Action
from .. import Color, Peg, Board

class MoveAction(Action):
    def __init__(self, die_roll: int, color: Color):
        self.die_roll = die_roll
        self.color = color

    def get_applicable_pegs(self, board: Board) -> List[Peg]:
        applicable_pegs: List[Peg] = []

        pegs = board.get_pegs_by_color(self.color)
        for peg in pegs:
            # skip if peg is on deck
            if board.is_peg_on_deck(peg):
                continue

            current_track_position = board.get_track_position_for_peg(peg)
            assert current_track_position is not None

            # skip if it would push us off the end of our track
            new_track_position = current_track_position + self.die_roll
            if new_track_position >= Board.FULL_TRACK_LENGTH:
                continue

            # skip if we would land on our own peg
            other_peg = board.get_peg_at_track_position(new_track_position, self.color)
            if other_peg is not None:
                continue

            applicable_pegs.append(peg)
        return applicable_pegs

    def apply(self, peg: Peg, board: Board) -> Board:
        current_track_position = board.get_track_position_for_peg(peg)
        assert current_track_position is not None

        new_track_position = current_track_position + self.die_roll

        # bump any peg in the way to on deck
        new_board_position = board.track_position_to_board_position(new_track_position, self.color)
        if new_board_position is not None:
            other_peg = board.get_peg_at_board_position(new_board_position)
            if other_peg is not None:
                board.set_peg_on_deck(other_peg)

        # move peg
        board.set_peg_track_position(peg, new_track_position)

        return board