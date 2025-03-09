from trouble import Board, Color, Peg
from trouble.models import BoardModel

class TestBoardModel:
    class TestFromBoard:
        def test_from_board(self):
            board = Board()
            board.add_peg(Peg(1, Color.RED))
            board.add_peg_at_track_position(Peg(2, Color.BLUE), 0)
            board.add_peg_at_track_position(Peg(3, Color.GREEN), Board.FULL_TRACK_LENGTH - 1)

            model = BoardModel.from_board(board)

            assert model.on_deck == ["R"]
            assert model.color_by_board_position == {21: "B"}
            assert model.final_slots == ["G"]