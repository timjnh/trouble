from trouble.gameplay import Board, Color, Peg
from trouble.generation import BoardModel

class TestBoardModel:
    class TestFromBoard:
        def test_from_board(self):
            board = Board()
            board.add_peg(Peg(1, Color.RED))
            board.add_peg_at_track_position(Peg(2, Color.BLUE), 1)
            board.add_peg_at_track_position(Peg(3, Color.BLUE), 0)
            board.add_peg_at_track_position(Peg(4, Color.GREEN), Board.FULL_TRACK_LENGTH - 1)

            model = BoardModel.from_board(board)

            assert model.red == [-1] # on deck is -1
            assert model.green == [Board.FULL_TRACK_LENGTH - 1]
            assert model.yellow == []
            assert model.blue == [1, 0] # should be ordered by peg id