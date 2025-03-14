from random import random
from typing import List

from .action_selector import ActionSelector, SelectedAction
from .board import Board
from .color import Color 
from .actions import Action, MoveToBoardAction, MoveAction, NoneAction

class RandomActionSelector(ActionSelector):
    def select_action(self, color: Color, board: Board, die_roll: int, color_turns: int) -> SelectedAction:
        possible_actions: List[Action] = [
            MoveToBoardAction(die_roll, color),
            MoveAction(die_roll, color)
        ]

        possible_actions.sort(key=lambda x: random())

        for action in possible_actions:
            pegs = action.get_applicable_pegs(board)
            if len(pegs) > 0:
                pegs.sort(key=lambda x: random())
                return SelectedAction(action, pegs[0])

        return SelectedAction(NoneAction(), None)