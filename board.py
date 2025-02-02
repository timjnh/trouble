from typing import List, Dict

from peg import Peg
from color import Color

class Board:
    FULL_TRACK_LENGTH = 32 # includes the final four slots
    INTERIOR_TRACK_LENGTH = FULL_TRACK_LENGTH - 4

    def __init__(self):
        self.pegs_by_color: Dict[Color, List[Peg]] = {}

    def reset(self):
        for c in Color:
            if self.pegs_by_color.get(c) is not None:
                for p in self.pegs_by_color[c]:
                    p.reset()

    def add_pegs(self, pegs: List[Peg]):
        for p in pegs:
            if p.color not in self.pegs_by_color:
                self.pegs_by_color[p.color] = []
            self.pegs_by_color[p.color].append(p)

    @property
    def pegs(self) -> List[Peg]:
        return [peg for peg_list in self.pegs_by_color.values() for peg in peg_list]

    def get_pegs_on_deck(self, color: Color) -> List[Peg]:
        return [p for p in self.pegs_by_color[color] if p.is_on_deck]
    
    def get_pegs_in_final_slots(self, color: Color) -> List[Peg]:
        if self.pegs_by_color.get(color) is None:
            return []
        return [p for p in self.pegs_by_color[color] if p.position is not None and p.position >= self.FULL_TRACK_LENGTH - 4]