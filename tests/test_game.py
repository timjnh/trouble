from trouble import Game, Board, Peg, Color, DefaultDie, RandomActionSelector, MoveToBoardAction, SelectedAction, MoveAction
from mock_action_selector import MockActionSelector
from mock_die import MockDie

class TestGame:
    class TestReset:
        def test_should_reset_the_board_and_set_current_color_to_red(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            game = Game(board, RandomActionSelector(), DefaultDie())

            game.reset()

            assert game.current_color == Color.RED
            assert len(board.get_pegs_on_deck(Color.RED)) == 1

    class TestWinner:
        def test_returns_the_color_where_all_final_slots_are_full(self):
            board = Board()

            red_pegs = [Peg(Color.RED) for _ in range(4)]
            for i, peg in enumerate(red_pegs):
                board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - (i + 1))

            game = Game(board, RandomActionSelector(), DefaultDie())

            assert game.winner == Color.RED

        def test_returns_none_when_no_color_has_all_four_final_slots_full(self):
            board = Board()

            red_pegs = [Peg(Color.RED) for _ in range(4)]
            for i, peg in enumerate(red_pegs):
                board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - (i + 2)) # only 3 in final slots

            game = Game(board, RandomActionSelector(), DefaultDie())

            assert game.winner == None

        def test_returns_none_when_board_has_no_pegs(self):
            board = Board()
            game = Game(board, RandomActionSelector(), DefaultDie())

            assert game.winner is None

    class TestTakeTurn:
        def test_should_move_the_current_color_based_on_the_die_roll(self):
            red_peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, 0)

            actions = [
                SelectedAction(
                    MoveAction(1, Color.RED, board),
                    red_peg
                )
            ]
            game = Game(board, MockActionSelector(actions), MockDie([1]))

            game.take_turn()

            assert game.current_color == Color.GREEN
            assert board.get_track_position_for_peg(red_peg) == 1

        def test_should_not_advance_the_current_color_if_a_6_is_rolled(self):
            red_peg = Peg(Color.RED)

            board = Board()
            board.add_peg(red_peg)

            actions = [
                SelectedAction(
                    MoveToBoardAction(6, Color.RED, board),
                    red_peg
                )
            ]
            game = Game(board, MockActionSelector(actions), MockDie([6]))

            game.take_turn()

            assert game.current_color == Color.RED
            assert board.get_track_position_for_peg(red_peg) == 0

        def test_should_not_advance_the_current_color_if_the_peg_lands_on_a_double_turn_location(self):
            red_peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, 0)

            actions = [
                SelectedAction(
                    MoveAction(3, Color.RED, board),
                    red_peg
                )
            ]
            game = Game(board, MockActionSelector(actions), MockDie([3]))

            game.take_turn()

            assert game.current_color == Color.RED
            assert board.get_track_position_for_peg(red_peg) == 3

        def test_should_give_two_extra_turns_for_a_6_and_a_double_turn_location(self):
            red_peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, 4)

            actions = [
                SelectedAction(
                    MoveAction(6, Color.RED, board),
                    red_peg
                ),
                SelectedAction(
                    MoveAction(1, Color.RED, board),
                    red_peg
                ),
                SelectedAction(
                    MoveAction(1, Color.RED, board),
                    red_peg
                )
            ]
            game = Game(board, MockActionSelector(actions), MockDie([6, 1, 1]))

            game.take_turn()

            assert game.current_color == Color.RED
            assert board.get_track_position_for_peg(red_peg) == 10

            game.take_turn()

            assert game.current_color == Color.RED
            assert board.get_track_position_for_peg(red_peg) == 11

            game.take_turn()

            assert game.current_color == Color.GREEN
            assert board.get_track_position_for_peg(red_peg) == 12

