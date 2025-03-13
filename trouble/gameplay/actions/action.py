from abc import ABC, abstractmethod
from typing import List

from .. import Peg, Board

class Action(ABC):
    @abstractmethod
    def get_applicable_pegs(self, board: Board) -> List[Peg]:
        pass

    @abstractmethod
    def apply(self, peg: Peg, board: Board) -> Board:
        pass