from .action import Action
from ..peg import Peg

class MoveToBoardAction(Action):
    def __init__(self, peg: Peg):
        self.peg = peg

    def apply(self):
        self.peg.position = 0

        # TODO: bounce any pegs at our start position to on deck