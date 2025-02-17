from .action_selector import ActionSelector
from .board import Board
from .color import Color
from .actions import Action, MoveToBoardAction, NoneAction

class DefaultActionSelector(ActionSelector):
    def select_action(self, color: Color, board: Board) -> Action:
        die_roll = self.die.roll()

        # TODO: randomize the behavior here
        if die_roll == 6:
            global_starting_position = board.get_global_peg_position_for_color(0, color)
            peg_at_starting_position = board.get_peg_at_global_position(global_starting_position)

            on_deck_pegs = board.get_pegs_on_deck(color)
            if (peg_at_starting_position is None or peg_at_starting_position.color != color) and len(on_deck_pegs) > 0:
                return MoveToBoardAction(on_deck_pegs[0], board)

        return NoneAction()