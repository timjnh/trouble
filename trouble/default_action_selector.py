from .action_selector import ActionSelector
from .board import Board
from .color import Color
from .actions import Action, MoveToBoardAction, NoneAction

class DefaultActionSelector(ActionSelector):
    def select_action(self, color: Color, board: Board) -> Action:
        die_roll = self.die.roll()

        # TODO: randomize the behavior here
        if die_roll == 6:
            on_deck_pegs = board.get_pegs_on_deck(color)
            if len(on_deck_pegs) > 0:
                return MoveToBoardAction(on_deck_pegs[0])

        return NoneAction()