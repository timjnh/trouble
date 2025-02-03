from trouble import Color

class TestColor:
    class TestOrdinal:
        def test_ordinal_returns_the_index_of_the_given_color(self):
            assert Color.ordinal(Color.RED) == 0
            assert Color.ordinal(Color.GREEN) == 1
            assert Color.ordinal(Color.YELLOW) == 2
            assert Color.ordinal(Color.BLUE) == 3

    class TestNext:
        def test_next_returns_the_next_color_in_the_sequence(self):
            assert Color.next(Color.RED) == Color.GREEN
            assert Color.next(Color.GREEN) == Color.YELLOW
            assert Color.next(Color.YELLOW) == Color.BLUE
            assert Color.next(Color.BLUE) == Color.RED