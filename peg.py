from color import Color

class Peg:
  def __init__(self, color: Color):
    self.color = color
    self.is_on_board = False
    self.position: int | None = None