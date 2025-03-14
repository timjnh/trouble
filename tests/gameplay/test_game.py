import pytest

from trouble.gameplay import Game, Board, Peg, Color, DefaultDie, RandomActionSelector, MoveToBoardAction, SelectedAction, MoveAction, ActionSelector
from mock_action_selector import MockActionSelector
from mock_die import MockDie

class TestGame:
    @pytest.fixture
    def action_selectors(self):
        return { color: RandomActionSelector() for color in Color }

    class TestReset:
        def test_should_reset_the_board(self, action_selectors):
            peg = Peg(1, Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            game = Game(board, action_selectors, DefaultDie())

            game.reset()

            assert len(board.get_pegs_on_deck(Color.RED)) == 1

    class TestWinner:
        def test_returns_the_color_where_all_final_slots_are_full(self, action_selectors):
            board = Board()

            red_pegs = [Peg(i, Color.RED) for i in range(4)]
            for i, peg in enumerate(red_pegs):
                board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - (i + 1))

            game = Game(board, action_selectors, DefaultDie())

            assert game.winner == Color.RED

        def test_returns_none_when_no_color_has_all_four_final_slots_full(self, action_selectors):
            board = Board()

            red_pegs = [Peg(i, Color.RED) for i in range(4)]
            for i, peg in enumerate(red_pegs):
                board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - (i + 2)) # only 3 in final slots

            game = Game(board, action_selectors, DefaultDie())

            assert game.winner == None

        def test_returns_none_when_board_has_no_pegs(self, action_selectors):
            board = Board()
            game = Game(board, action_selectors, DefaultDie())

            assert game.winner is None

    class TestTakeTurn:
        def test_should_move_the_current_color_based_on_the_die_roll(self):
            red_peg = Peg(1, Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, 0)

            actions = [
                SelectedAction(
                    MoveAction(1, Color.RED),
                    red_peg
                )
            ]
            action_selector = MockActionSelector(actions)
            action_selectors: dict[Color, ActionSelector] = { color: action_selector for color in Color }
            game = Game(board, action_selectors, MockDie([1]))

            game.take_turn()

            assert game.current_color == Color.GREEN
            assert game.current_color_turns == 1
            assert board.get_track_position_for_peg(red_peg) == 1

        def test_should_not_advance_the_current_color_if_a_6_is_rolled(self):
            red_peg = Peg(1, Color.RED)

            board = Board()
            board.add_peg(red_peg)

            actions = [
                SelectedAction(
                    MoveToBoardAction(6, Color.RED),
                    red_peg
                )
            ]
            action_selector = MockActionSelector(actions)
            action_selectors: dict[Color, ActionSelector] = { color: action_selector for color in Color }
            game = Game(board, action_selectors, MockDie([6]))

            game.take_turn()

            assert game.current_color == Color.RED
            assert board.get_track_position_for_peg(red_peg) == 0

        def test_should_not_advance_the_current_color_if_the_peg_lands_on_a_double_turn_location(self):
            red_peg = Peg(1, Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, 0)

            actions = [
                SelectedAction(
                    MoveAction(3, Color.RED),
                    red_peg
                )
            ]
            action_selector = MockActionSelector(actions)
            action_selectors: dict[Color, ActionSelector] = { color: action_selector for color in Color }
            game = Game(board, action_selectors, MockDie([3]))

            game.take_turn()

            assert game.current_color == Color.RED
            assert board.get_track_position_for_peg(red_peg) == 3

        def test_should_give_two_extra_turns_for_a_6_and_a_double_turn_location(self):
            red_peg = Peg(1, Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, 4)

            actions = [
                SelectedAction(
                    MoveAction(6, Color.RED),
                    red_peg
                ),
                SelectedAction(
                    MoveAction(1, Color.RED),
                    red_peg
                ),
                SelectedAction(
                    MoveAction(1, Color.RED),
                    red_peg
                )
            ]
            action_selector = MockActionSelector(actions)
            action_selectors: dict[Color, ActionSelector] = { color: action_selector for color in Color }
            game = Game(board, action_selectors, MockDie([6, 1, 1]))

            game.take_turn()

            assert game.current_color == Color.RED
            assert board.get_track_position_for_peg(red_peg) == 10

            game.take_turn()

            assert game.current_color == Color.RED
            assert board.get_track_position_for_peg(red_peg) == 11

            game.take_turn()

            assert game.current_color == Color.GREEN
            assert board.get_track_position_for_peg(red_peg) == 12

