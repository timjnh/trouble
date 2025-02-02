from typing import List, Dict

from peg import Peg
from color import Color

class Board:
  def __init__(self):
    self.pegs_by_color: Dict[Color, List[Peg]] = {}

  def reset(self):
    for c in Color:
      self.pegs_by_color[c] = [Peg(c) for _ in range(4)]

  @property
  def pegs(self) -> List[Peg]:
    return [peg for peg_list in self.pegs_by_color.values() for peg in peg_list]

  def get_on_deck_pegs_of_color(self, color: Color) -> List[Peg]:
    return [p for p in self.pegs_by_color[color] if not p.is_on_board]