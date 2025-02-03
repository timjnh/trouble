from trouble import Game, Board, Peg, Color, DefaultActionSelector, DefaultDie
from mock_die import MockDie

class TestGame:
    class TestReset:
        def test_should_reset_the_board_and_set_current_color_to_red(self):
            peg = Peg(Color.RED)
            peg.position = 0

            board = Board()
            board.add_pegs([peg])

            game = Game(board, DefaultActionSelector(DefaultDie()))

            game.reset()

            assert game.current_color == Color.RED
            assert len(board.get_pegs_on_deck(Color.RED)) == 1

    class TestWinner:
        def test_returns_the_color_where_all_final_slots_are_full(self):
            board = Board()

            red_pegs = [Peg(Color.RED) for _ in range(4)]
            for i, peg in enumerate(red_pegs):
                peg.position = Board.FULL_TRACK_LENGTH - (i + 1)

            board.add_pegs(red_pegs)

            game = Game(board, DefaultActionSelector(DefaultDie()))

            assert game.winner == Color.RED

        def test_returns_none_when_no_color_has_all_four_final_slots_full(self):
            board = Board()

            red_pegs = [Peg(Color.RED) for _ in range(4)]
            for i, peg in enumerate(red_pegs):
                peg.position = Board.FULL_TRACK_LENGTH - (i + 2) # only 3 in final slots

            board.add_pegs(red_pegs)

            game = Game(board, DefaultActionSelector(DefaultDie()))

            assert game.winner == None

        def test_returns_none_when_board_has_no_pegs(self):
            board = Board()
            game = Game(board, DefaultActionSelector(DefaultDie()))

            assert game.winner is None

    class TestTakeTurn:
        def test_should_advance_the_next_color_by_the_die_roll(self):
            pegs = [[Peg(c) for _ in range(4)] for c in Color]

            board = Board()
            board.add_pegs([peg for color_pegs in pegs for peg in color_pegs])

            # TODO: implement a MockActionSelector that will always return particular actions
            game = Game(board, DefaultActionSelector(MockDie(rolls=[6])))

            game.take_turn()

            assert game.current_color == Color.GREEN
            assert len(board.get_pegs_on_deck(Color.RED)) == 3
            
            pegs_on_board = board.get_pegs_on_board(Color.RED)
            assert len(pegs_on_board) == 1
            assert pegs_on_board[0].position == 0