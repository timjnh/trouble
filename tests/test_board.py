from board import Board
from color import Color

class TestBoard:
  class TestReset:
    def test_all_pegs_start_as_on_deck(self):
      board = Board()
      board.reset()

      assert len(board.pegs) == 16

      for c in Color:
        assert len(board.get_on_deck_pegs_of_color(c)) == 4