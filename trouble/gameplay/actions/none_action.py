from typing import List

from .. import Peg, Board
from .action import Action

class NoneAction(Action):
    def get_applicable_pegs(self, board: Board) -> List[Peg]:
        return []

    def apply(self, peg: Peg, board: Board) -> Board:
        return board