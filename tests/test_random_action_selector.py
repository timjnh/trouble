from trouble import Board, Color, RandomActionSelector
from trouble.actions import NoneAction

class TestRandomActionSelector:
    class TestSelectAction:
        def test_should_return_none_action_if_no_actions_are_possible(self):
            board = Board()

            selector = RandomActionSelector()
            selected_action = selector.select_action(Color.RED, board, 1)
            assert isinstance(selected_action.action, NoneAction)
            assert selected_action.peg is None
