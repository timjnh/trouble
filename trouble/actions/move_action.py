from typing import List

from .action import Action
from .. import Color, Peg, Board

class MoveAction(Action):
    def __init__(self, die_roll: int, color: Color, board: Board):
        self.die_roll = die_roll
        self.color = color
        self.board = board

    def get_applicable_pegs(self) -> List[Peg]:
        applicable_pegs: List[Peg] = []

        pegs = self.board.get_pegs_by_color(self.color)
        for peg in pegs:
            # skip if peg is on deck
            if self.board.is_peg_on_deck(peg):
                continue

            current_track_position = self.board.get_track_position_for_peg(peg)
            assert current_track_position is not None

            # skip if it would push us off the end of our track
            new_track_position = current_track_position + self.die_roll
            if new_track_position >= Board.FULL_TRACK_LENGTH:
                continue

            # skip if we would land on our own peg
            other_peg = self.board.get_peg_at_track_position(new_track_position, self.color)
            if other_peg is not None:
                continue

            applicable_pegs.append(peg)
        return applicable_pegs

    def apply(self, peg: Peg):
        pass