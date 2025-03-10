from typing import List

from trouble import ActionSelector, SelectedAction, Color, Board

class MockActionSelector(ActionSelector):
    def __init__(self, actions: List[SelectedAction]):
        self.actions = actions
        self._position = 0

    def select_action(self, color: Color, board: Board, die_roll: int) -> SelectedAction:
        action = self.actions[self._position]
        if self._position < len(self.actions) - 1:
            self._position += 1
        return action