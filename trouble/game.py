import random

from .board import Board
from .color import Color
from .action_selector import ActionSelector
from .die import Die

class Game:
    def __init__(self, board: Board, action_selector: ActionSelector, die: Die):
        self.board = board
        self.action_selector = action_selector
        self.current_color = Color.RED
        self.current_color_turns = 1
        self.die = die

    def reset(self):
        self.board.reset()
        self.current_color = random.choice(list(Color))

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
        die_roll = self.die.roll()

        selected_action = self.action_selector.select_action(self.current_color, self.board, die_roll)
        selected_action.apply()

        if selected_action.peg is not None:
            board_position = self.board.get_board_position_for_peg(selected_action.peg)
            if board_position is not None and board_position % 7 == 3:
                self.current_color_turns += 1

        if die_roll == 6:
            self.current_color_turns += 1

        self.current_color_turns -= 1
        if self.current_color_turns == 0:
            self.current_color = Color.next(self.current_color)
            self.current_color_turns = 1