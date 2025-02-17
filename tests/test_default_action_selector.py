from trouble import Board, Color, DefaultActionSelector, Peg
from trouble.actions import MoveToBoardAction, NoneAction

from mock_die import MockDie

class TestDefaultActionSelector:
    class TestSelectAction:
        def test_should_return_move_to_board_if_a_6_is_rolled(self):
            die = MockDie(rolls=[6])

            peg = Peg(Color.RED)

            board = Board()
            board.add_pegs([peg])

            action_selector = DefaultActionSelector(die)
            action = action_selector.select_action(Color.RED, board)

            assert isinstance(action, MoveToBoardAction) == True

        def test_should_not_return_move_to_board_if_position_0_is_occupied_by_the_same_color(self):
            die = MockDie(rolls=[6])

            peg_1 = Peg(Color.RED)
            peg_1.position = 0

            peg_2 = Peg(Color.RED)

            board = Board()
            board.add_pegs([peg_1, peg_2])

            action_selector = DefaultActionSelector(die)
            action = action_selector.select_action(Color.RED, board)

            assert isinstance(action, NoneAction) == True

        def test_should_not_return_move_to_board_if_there_are_no_on_deck_pegs(self):
            pass

        def test_should_default_to_a_none_action(self):
            pass

