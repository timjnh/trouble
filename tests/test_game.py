from game import Game
from board import Board
from peg import Peg
from color import Color

class TestGame:
    class TestWinner:
        def test_returns_the_color_where_all_final_slots_are_full(self):
            board = Board()

            red_pegs = [Peg(Color.RED) for _ in range(4)]
            for i, peg in enumerate(red_pegs):
                peg.position = Board.FULL_TRACK_LENGTH - (i + 1)

            board.add_pegs(red_pegs)

            game = Game(board)

            assert game.winner == Color.RED

        def test_returns_none_when_no_color_has_all_four_final_slots_full(self):
            board = Board()

            red_pegs = [Peg(Color.RED) for _ in range(4)]
            for i, peg in enumerate(red_pegs):
                peg.position = Board.FULL_TRACK_LENGTH - (i + 2) # only 3 in final slots

            board.add_pegs(red_pegs)

            game = Game(board)

            assert game.winner == None

        def test_returns_none_when_board_has_no_pegs(self):
            board = Board()
            game = Game(board)

            assert game.winner is None