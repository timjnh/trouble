from trouble import Board, Color, RandomActionSelector, Peg
from trouble.actions import MoveToBoardAction, NoneAction

from mock_die import MockDie

class TestRandomActionSelector:
    class TestSelectAction:
        def test_should_return_move_to_board_if_a_6_is_rolled(self):
            die = MockDie(rolls=[6])

            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            action_selector = RandomActionSelector(die)
            action = action_selector.select_action(Color.RED, board)

            assert isinstance(action, MoveToBoardAction) == True

        def test_should_not_return_move_to_board_if_position_0_is_occupied_by_the_same_color(self):
            die = MockDie(rolls=[6])

            peg_1 = Peg(Color.RED)
            peg_2 = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg_1, 0)
            board.add_peg(peg_2)

            action_selector = RandomActionSelector(die)
            action = action_selector.select_action(Color.RED, board)

            assert isinstance(action, NoneAction) == True

        def test_should_not_return_move_to_board_if_there_are_no_on_deck_pegs(self):
            die = MockDie(rolls=[6])

            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            action_selector = RandomActionSelector(die)
            action = action_selector.select_action(Color.RED, board)

            assert isinstance(action, NoneAction) == True

        def test_should_default_to_a_none_action(self):
            die = MockDie(rolls=[1])

            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            action_selector = RandomActionSelector(die)
            action = action_selector.select_action(Color.RED, board)

            assert isinstance(action, NoneAction) == True

