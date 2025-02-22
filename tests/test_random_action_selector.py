from trouble import Board, Color, RandomActionSelector
from trouble.actions import NoneAction

from mock_die import MockDie

class TestRandomActionSelector:
    class TestSelectAction:
        def test_should_return_none_action_if_no_actions_are_possible(self):
            die = MockDie([1])
            board = Board()

            selector = RandomActionSelector(die)
            selected_action = selector.select_action(Color.RED, board)
            assert isinstance(selected_action.action, NoneAction)
            assert selected_action.peg is None
