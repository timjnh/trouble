from abc import ABC, abstractmethod
from dataclasses import dataclass

from .color import Color
from .board import Board
from .actions import Action
from .peg import Peg

@dataclass
class SelectedAction:
    action: Action
    peg: Peg | None

    def __init__(self, action: Action, peg: Peg | None):
        self.action = action
        self.peg = peg

    def apply(self, board: Board):
        if self.peg is not None:
            self.action.apply(self.peg, board)

class ActionSelector(ABC):
    @abstractmethod
    def select_action(self, color: Color, board: Board, die_roll: int) -> SelectedAction:
        pass