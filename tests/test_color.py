from trouble.gameplay import Color

class TestColor:
    class TestOrdinal:
        def test_ordinal_returns_the_index_of_the_given_color(self):
            assert Color.ordinal(Color.RED) == 0
            assert Color.ordinal(Color.GREEN) == 1
            assert Color.ordinal(Color.YELLOW) == 2
            assert Color.ordinal(Color.BLUE) == 3

    class TestFromOrdinal:
        def test_from_ordinal_returns_the_color_at_the_given_index(self):
            assert Color.from_ordinal(0) == Color.RED
            assert Color.from_ordinal(1) == Color.GREEN
            assert Color.from_ordinal(2) == Color.YELLOW
            assert Color.from_ordinal(3) == Color.BLUE

    class TestFromString:
        def test_from_string_returns_the_color_for_the_given_string(self):
            assert Color.from_string('R') == Color.RED
            assert Color.from_string('G') == Color.GREEN
            assert Color.from_string('Y') == Color.YELLOW
            assert Color.from_string('B') == Color.BLUE

    class TestNext:
        def test_next_returns_the_next_color_in_the_sequence(self):
            assert Color.next(Color.RED) == Color.GREEN
            assert Color.next(Color.GREEN) == Color.YELLOW
            assert Color.next(Color.YELLOW) == Color.BLUE
            assert Color.next(Color.BLUE) == Color.RED