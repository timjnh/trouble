from random import random

from .action_selector import ActionSelector
from .board import Board
from .color import Color
from .actions import Action, MoveToBoardAction, NoneAction

class RandomActionSelector(ActionSelector):
    def select_action(self, color: Color, board: Board) -> Action:
        die_roll = self.die.roll()

        possible_actions = [
            MoveToBoardAction(die_roll, color, board)
        ]

        possible_actions.sort(key=lambda x: random())

        for action in possible_actions:
            if action.is_applicable():
                return action

        return NoneAction()