from color import Color

class TestColor:
    class TestOrdinal:
        def test_ordinal_returns_the_index_of_the_given_color(self):
            assert Color.ordinal(Color.RED) == 0
            assert Color.ordinal(Color.GREEN) == 1
            assert Color.ordinal(Color.YELLOW) == 2
            assert Color.ordinal(Color.BLUE) == 3