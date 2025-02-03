from abc import ABC, abstractmethod

from .color import Color
from .board import Board
from .die import Die
from .actions import Action

class ActionSelector(ABC):
    def __init__(self, die: Die):
        self.die = die

    @abstractmethod
    def select_action(self, color: Color, board: Board) -> Action:
        pass