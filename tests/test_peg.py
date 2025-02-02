from peg import Peg
from color import Color

class TestPeg:
    class TestIsOnboard:
        def test_is_on_board_if_position_if_not_none(self):
            peg = Peg(Color.RED)
            peg.position = 0
            assert peg.is_on_board

        def test_is_not_on_board_if_position_is_none(self):
            peg = Peg(Color.RED)
            assert peg.position is None
            assert not peg.is_on_board

    class TestReset:
        def test_resets_position_to_none(self):
            peg = Peg(Color.RED)
            peg.position = 0
            peg.reset()
            assert peg.position == None