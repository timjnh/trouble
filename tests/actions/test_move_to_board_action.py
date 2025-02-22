from trouble import Color, Peg, MoveToBoardAction, Board

class TestMoveToBoardAction:
    class TestApply:
        def test_should_move_peg_to_position_zero_on_their_track(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            action = MoveToBoardAction(peg, board)
            action.apply()

            assert board.get_track_position_for_peg(peg) == 0

        def test_should_bounce_any_pegs_at_start_position_to_on_deck(self):
            red_peg = Peg(Color.RED)
            green_peg = Peg(Color.GREEN)

            board = Board()
            board.add_peg(red_peg)

            red_board_start_position = board.track_position_to_board_position(0, Color.RED)
            assert red_board_start_position is not None
            green_track_position = board.board_position_to_track_position(red_board_start_position, Color.GREEN)
            board.add_peg_at_track_position(green_peg, green_track_position)

            action = MoveToBoardAction(red_peg, board)
            action.apply()

            assert board.is_peg_on_deck(green_peg)