from trouble import Color, Peg, MoveAction, Board

class TestMoveAction:
    class TestIsApplicable:
        def test_should_return_true_if_there_is_a_peg_with_nothing_blocking_it(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            action = MoveAction(1, Color.RED, board)
            assert action.is_applicable() == True

        def test_should_return_false_if_there_are_no_pegs_on_the_board(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            action = MoveAction(1, Color.RED, board)
            assert action.is_applicable() == False

        def test_should_return_false_if_moving_would_take_the_peg_off_their_track(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - 1)

            action = MoveAction(1, Color.RED, board)
            assert action.is_applicable() == False

        # TODO: i think we should establish the peg here.  maybe get_applicable_peg
        def test_should_return_false_if_we_would_land_on_our_own_peg(self):
            peg1 = Peg(Color.RED)
            peg2 = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg1, Board.FULL_TRACK_LENGTH - 3)
            board.add_peg_at_track_position(peg2, Board.FULL_TRACK_LENGTH - 6)

            action = MoveAction(3, Color.RED, board)
            assert action.is_applicable() == False

        def test_should_return_true_if_we_would_land_on_someone_elses_peg(self):
            red_peg = Peg(Color.RED)
            green_peg = Peg(Color.GREEN)

            board = Board()
            board.add_peg_at_track_position(red_peg, 0)

            red_start_board_position = board.track_position_to_board_position(0, Color.RED)
            assert red_start_board_position is not None
            green_track_position = board.board_position_to_track_position(red_start_board_position, Color.GREEN) + 1
            board.add_peg_at_track_position(green_peg, green_track_position)

            action = MoveAction(1, Color.RED, board)
            assert action.is_applicable() == True

        def test_should_return_true_if_at_least_one_of_our_pegs_can_move(self):
            peg1 = Peg(Color.RED)
            peg2 = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg1, 0)
            board.add_peg_at_track_position(peg2, 1)

            action = MoveAction(1, Color.RED, board)
            assert action.is_applicable() == True

        def test_should_return_true_even_if_we_are_in_final_slots(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - 2)

            action = MoveAction(1, Color.RED, board)
            assert action.is_applicable() == True
            