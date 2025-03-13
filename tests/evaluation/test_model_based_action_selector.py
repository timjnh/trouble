import numpy

from typing import List
from numpy.typing import NDArray

from trouble.evaluation import ModelBasedActionSelector
from trouble.training import Model
from trouble.gameplay import Board, Color, Peg, MoveAction, NoneAction

class MockModel(Model):
    def __init__(self, predictions: List[float]):
        super().__init__(id="MockModel")
        self._predictions = predictions
        self._prediction_calls = 0

    def build(self):
        pass

    def predict(self, X: NDArray[numpy.int8]) -> numpy.float32:
        assert self._prediction_calls < len(self._predictions)
        prediction = self._predictions[self._prediction_calls]

        self._prediction_calls += 1

        return numpy.float32(prediction)

class TestModelBasedActionSelector:
    class TestSelectAction:
        def test_should_evaluate_all_possible_moves_against_the_model(self):
            model = MockModel([0.7, 0.5])
            selector = ModelBasedActionSelector(model, 1)

            red_peg_1 = Peg(1, Color.RED)
            red_peg_2 = Peg(2, Color.RED)
            red_peg_3 = Peg(3, Color.RED)
            red_peg_4 = Peg(4, Color.RED)

            board = Board()
            board.add_peg(red_peg_1) # can't be moved because it's on deck
            board.add_peg_at_track_position(red_peg_2, 0) # can't be moved because red_peg_3 is in the way
            board.add_peg_at_track_position(red_peg_3, 3)
            board.add_peg_at_track_position(red_peg_4, 7)

            for color in [Color.BLUE, Color.GREEN, Color.YELLOW]:
                for i in range(4):
                    board.add_peg(Peg(5 + i + (4 * Color.ordinal(color)), color))

            action = selector.select_action(Color.RED, board, 3)

            assert action.peg == red_peg_3
            assert isinstance(action.action, MoveAction)

        def test_should_return_a_none_action_if_no_actions_are_possible(self):
            model = MockModel([0.7, 0.5])
            selector = ModelBasedActionSelector(model, 1)

            board = Board()
            for color in [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW]:
                for i in range(4):
                    board.add_peg(Peg(i + (4 * Color.ordinal(color)), color))

            action = selector.select_action(Color.RED, board, 3)

            assert isinstance(action.action, NoneAction)

    class TestEvaluatePossibleActions:
        def test_should_return_a_sorted_listed_of_evaluated_actions(self):
            model = MockModel([0.7, 0.5])
            selector = ModelBasedActionSelector(model, 1)

            red_peg_1 = Peg(1, Color.RED)
            red_peg_2 = Peg(2, Color.RED)
            red_peg_3 = Peg(3, Color.RED)
            red_peg_4 = Peg(4, Color.RED)

            board = Board()
            board.add_peg(red_peg_1) # can't be moved because it's on deck
            board.add_peg_at_track_position(red_peg_2, 0) # can't be moved because red_peg_3 is in the way
            board.add_peg_at_track_position(red_peg_3, 3)
            board.add_peg_at_track_position(red_peg_4, 7)

            for color in [Color.BLUE, Color.GREEN, Color.YELLOW]:
                for i in range(4):
                    board.add_peg(Peg(5 + i + (4 * Color.ordinal(color)), color))

            actions = selector.evaluate_possible_actions(Color.RED, board, 3)

            assert actions[0].prediction == 0.7
            assert actions[0].peg == red_peg_3
            assert actions[1].prediction == 0.5
            assert actions[1].peg == red_peg_4