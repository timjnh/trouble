from random import random
from typing import List

from .action_selector import ActionSelector
from .board import Board
from .color import Color
from .actions import Action, MoveToBoardAction, MoveAction, NoneAction

class RandomActionSelector(ActionSelector):
    def select_action(self, color: Color, board: Board) -> Action:
        die_roll = self.die.roll()

        # TODO: two turns if we roll a 6

        possible_actions: List[Action] = [
            MoveToBoardAction(die_roll, color, board),
            MoveAction(die_roll, color, board)
        ]

        possible_actions.sort(key=lambda x: random())

        for action in possible_actions:
            if action.is_applicable():
                return action

        return NoneAction()