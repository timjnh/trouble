from trouble import Color, Peg, MoveToBoardAction, Board

class TestMoveToBoardAction:
    class TestApply:
        def test_should_move_peg_to_position_zero_on_their_track(self):
            peg = Peg(Color.RED)
            assert peg.position is None

            board = Board()
            board.add_pegs([peg])

            action = MoveToBoardAction(peg, board)
            action.apply()

            assert peg.position == 0

        def test_should_bounce_any_pegs_at_start_position_to_on_deck(self):
            red_peg = Peg(Color.RED)
            assert red_peg.position is None

            green_peg = Peg(Color.GREEN)

            board = Board()
            board.add_pegs([red_peg, green_peg])

            red_board_start_position = board.track_position_to_board_position(0, Color.RED)
            green_peg.position = board.board_position_to_track_position(red_board_start_position, Color.GREEN)

            action = MoveToBoardAction(red_peg, board)
            action.apply()

            assert green_peg.is_on_deck