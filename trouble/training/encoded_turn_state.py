import numpy
from numpy.typing import NDArray

from ..models import TurnModel
from .. import Color

class EncodedTurnState:
    # Current color + number of turns + location of all 16 pegs
    SIZE = 1 + 1 + 16

    @classmethod
    def encode(cls, turn: TurnModel) -> NDArray[numpy.int8]:
        encoded = numpy.zeros(cls.SIZE, dtype=numpy.int8)

        encoded[0] = Color.ordinal(Color.from_string(turn.color))
        encoded[1] = turn.color_turns

        for color in Color:
            color_index = (4 * Color.ordinal(color)) + 2
            encoded[color_index:color_index + 4] = turn.board.model_dump()[color.lower()]

        return encoded