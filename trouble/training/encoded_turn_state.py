import numpy
from numpy.typing import NDArray
from typing import Dict, List

from ..generation import TurnModel
from ..gameplay import Color

class EncodedTurnState:
    # Current color + number of turns + location of all 16 pegs
    SIZE = 1 + 1 + 16

    @classmethod
    def encode(cls, color: Color, color_turns: int, track_positions: Dict[Color, List[int]]) -> NDArray[numpy.int8]:
        encoded = numpy.zeros(cls.SIZE, dtype=numpy.int8)

        encoded[0] = Color.ordinal(color)
        encoded[1] = color_turns

        for color in Color:
            color_index = (4 * Color.ordinal(color)) + 2
            encoded[color_index:color_index + 4] = track_positions[color]

        return encoded