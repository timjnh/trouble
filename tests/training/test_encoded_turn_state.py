import numpy
from typing import Dict, List

from trouble.generation import TurnModel, BoardModel
from trouble.training import EncodedTurnState
from trouble.gameplay import Color

class TestEncodedTurnState:
    class TestEncode:
        def test_should_encode_the_turn_state(self):
            track_positions: Dict[Color, List[int]] = {
                Color.RED: [1, 2, 3, 4],
                Color.GREEN: [1, 2, 3, -1],
                Color.YELLOW: [-1, 31, 0, 1],
                Color.BLUE: [-1, -1, 0, 1]
            }

            encoded = EncodedTurnState.encode(Color.RED, 2, track_positions)

            assert numpy.array_equal(encoded, [Color.ordinal(Color.RED), 2, 1, 2, 3, 4, 1, 2, 3, -1, -1, 31, 0, 1, -1, -1, 0, 1])