from abc import ABC, abstractmethod
from typing import List

from .. import Peg

class Action(ABC):
    @abstractmethod
    def get_applicable_pegs(self) -> List[Peg]:
        pass

    @abstractmethod
    def apply(self, peg: Peg):
        pass