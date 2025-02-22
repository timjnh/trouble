from typing import List, Dict

from trouble import Game, Board, Peg, Color, DefaultDie, DefaultActionSelector, MoveToBoardAction
from mock_action_selector import MockActionSelector

class TestGame:
    class TestReset:
        def test_should_reset_the_board_and_set_current_color_to_red(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            game = Game(board, DefaultActionSelector(DefaultDie()))

            game.reset()

            assert game.current_color == Color.RED
            assert len(board.get_pegs_on_deck(Color.RED)) == 1

    class TestWinner:
        def test_returns_the_color_where_all_final_slots_are_full(self):
            board = Board()

            red_pegs = [Peg(Color.RED) for _ in range(4)]
            for i, peg in enumerate(red_pegs):
                board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - (i + 1))

            game = Game(board, DefaultActionSelector(DefaultDie()))

            assert game.winner == Color.RED

        def test_returns_none_when_no_color_has_all_four_final_slots_full(self):
            board = Board()

            red_pegs = [Peg(Color.RED) for _ in range(4)]
            for i, peg in enumerate(red_pegs):
                board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - (i + 2)) # only 3 in final slots

            game = Game(board, DefaultActionSelector(DefaultDie()))

            assert game.winner == None

        def test_returns_none_when_board_has_no_pegs(self):
            board = Board()
            game = Game(board, DefaultActionSelector(DefaultDie()))

            assert game.winner is None

    class TestTakeTurn:
        def test_should_move_the_next_color_based_on_the_die_roll(self):
            pegs: Dict[Color, List[Peg]] = {}
            for c in Color:
                pegs[c] = [Peg(c) for _ in range(4)]

            board = Board()
            for peg in [peg for color_pegs in pegs.values() for peg in color_pegs]:
                board.add_peg(peg)

            on_deck_red_peg = pegs[Color.RED][0]
            game = Game(board, MockActionSelector([MoveToBoardAction(on_deck_red_peg, board)]))

            game.take_turn()

            assert game.current_color == Color.GREEN
            assert len(board.get_pegs_on_deck(Color.RED)) == 3
            
            pegs_on_board = board.get_pegs_on_board(Color.RED)
            assert len(pegs_on_board) == 1
            assert board.get_track_position_for_peg(pegs_on_board[0]) == 0