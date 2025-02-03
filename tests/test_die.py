from trouble.die import Die

class TestDie:
    class Roll:
        def test_should_produce_a_random_number_between_1_and_the_number_of_sides(self):
            die = Die()
            assert 1 <= die.roll() <= 6