from typing import List, Optional

from trouble import ActionSelector, Action, Die, Color, Board, DefaultDie

class MockActionSelector(ActionSelector):
    def __init__(self, actions: List[Action], die: Optional[Die] = None):
        super().__init__(die or DefaultDie())

        self.actions = actions
        self._position = 0

    def select_action(self, color: Color, board: Board) -> Action:
        action = self.actions[self._position]
        if self._position < len(self.actions) - 1:
            self._position += 1
        return action