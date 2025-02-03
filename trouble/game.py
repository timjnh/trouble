from .board import Board
from .color import Color
from .action_selector import ActionSelector

class Game:
    def __init__(self, board: Board, action_selector: ActionSelector):
        self.board = board
        self.action_selector = action_selector
        self.current_color = Color.RED

    def reset(self):
        self.board.reset()
        self.current_color = Color.RED

    @property
    def winner(self) -> Color | None:
        for c in Color:
            if len(self.board.get_pegs_in_final_slots(c)) == 4:
                return c
        return None

    @property
    def is_complete(self) -> bool:
        return self.winner is not None
    
    def take_turn(self):
        action = self.action_selector.select_action(self.current_color, self.board)
        action.apply()

        self.current_color = Color.next(self.current_color)