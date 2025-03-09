import numpy

from ..models import GameDocument

class EncodedGameState:
    # Number of turns + location of all 16 pegs
    SIZE = 1 + 16

    @classmethod
    def encode(self, game: GameDocument) -> numpy.ndarray[numpy.int8]:
        pass