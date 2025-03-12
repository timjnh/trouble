import numpy

from trouble.generation import TurnModel, BoardModel
from trouble.training import EncodedTurnState
from trouble import Color

class TestEncodedBoardState:
    class TestEncode:
        def test_should_encode_the_turn_state(self):
            board = BoardModel(
                red=[1, 2, 3, 4],
                green=[1, 2, 3, -1],
                yellow=[-1, 31, 0, 1],
                blue=[-1, -1, 0, 1]
            )

            turn = TurnModel(
                color="R",
                color_turns=2,
                board=board,
                roll=6
            )

            encoded = EncodedTurnState.encode(turn)

            assert numpy.array_equal(encoded, [Color.ordinal(Color.RED), 2, 1, 2, 3, 4, 1, 2, 3, -1, -1, 31, 0, 1, -1, -1, 0, 1])