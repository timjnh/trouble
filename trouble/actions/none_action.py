from typing import List

from .. import Peg
from .action import Action

class NoneAction(Action):
    def get_applicable_pegs(self) -> List[Peg]:
        return []

    def apply(self, peg: Peg):
        pass