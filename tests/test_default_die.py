from trouble.default_die import DefaultDie

class TestDefaultDie:
    class TestRoll:
        def test_should_produce_a_random_number_between_1_and_the_number_of_sides(self):
            die = DefaultDie()
            assert 1 <= die.roll() <= 6