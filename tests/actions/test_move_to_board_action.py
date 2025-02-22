from trouble import Color, Peg, MoveToBoardAction, Board

class TestMoveToBoardAction:
    class TestIsApplicable:
        def test_should_return_true_if_die_roll_is_6_and_start_position_is_empty(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            action = MoveToBoardAction(6, Color.RED, board)
            assert action.is_applicable() == True

        def test_should_return_true_if_die_roll_is_6_and_start_position_is_occupied_by_another_color(self):
            red_peg = Peg(Color.RED)
            green_peg = Peg(Color.GREEN)

            board = Board()
            board.add_peg(red_peg)

            board_start_position = board.track_position_to_board_position(0, Color.RED)
            assert board_start_position is not None
            green_track_position = board.board_position_to_track_position(board_start_position, Color.GREEN)
            board.add_peg_at_track_position(green_peg, green_track_position)

            action = MoveToBoardAction(6, Color.RED, board)
            assert action.is_applicable() == True

        def test_should_return_false_if_die_roll_is_6_and_start_position_is_occupied_by_same_color(self):
            peg_1 = Peg(Color.RED)
            peg_2 = Peg(Color.RED)

            board = Board()
            board.add_peg(peg_1)
            board.add_peg_at_track_position(peg_2, 0)

            action = MoveToBoardAction(6, Color.RED, board)
            assert action.is_applicable() == False

        def test_should_return_false_if_die_roll_is_6_and_no_pegs_on_deck(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            action = MoveToBoardAction(6, Color.RED, board)
            assert action.is_applicable() == False

        def test_should_return_false_if_die_roll_is_not_6(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            action = MoveToBoardAction(5, Color.RED, board)
            assert action.is_applicable() == False

    class TestApply:
        def test_should_move_peg_to_position_zero_on_their_track(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            action = MoveToBoardAction(6, Color.RED, board)
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

            action = MoveToBoardAction(6, Color.RED, board)
            action.apply()

            assert board.is_peg_on_deck(green_peg)
            assert board.get_track_position_for_peg(red_peg) == 0