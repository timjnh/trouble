from trouble import Color, Peg, MoveAction, Board

class TestMoveAction:
    class TestGetApplicablePegs:
        def test_should_return_pegs_with_nothing_blocking_them(self):
            peg_1 = Peg(1, Color.RED)
            peg_2 = Peg(2, Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg_1, 0)
            board.add_peg_at_track_position(peg_2, 2)

            action = MoveAction(1, Color.RED, board)
            assert set(action.get_applicable_pegs()) == set([peg_1, peg_2])

        def test_should_an_empty_list_if_there_are_no_pegs_on_the_board(self):
            peg = Peg(1, Color.RED)

            board = Board()
            board.add_peg(peg)

            action = MoveAction(1, Color.RED, board)
            assert action.get_applicable_pegs() == []

        def test_should_not_return_pegs_that_would_move_off_the_track(self):
            peg = Peg(1, Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - 1)

            action = MoveAction(1, Color.RED, board)
            assert action.get_applicable_pegs() == []

        def test_should_not_return_pegs_that_would_land_on_our_own_pegs(self):
            peg1 = Peg(1, Color.RED)
            peg2 = Peg(2, Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg1, Board.FULL_TRACK_LENGTH - 3)
            board.add_peg_at_track_position(peg2, Board.FULL_TRACK_LENGTH - 6)

            action = MoveAction(3, Color.RED, board)
            assert action.get_applicable_pegs() == []

        def test_should_return_pegs_that_would_land_on_another_color_peg(self):
            red_peg = Peg(1, Color.RED)
            green_peg = Peg(2, Color.GREEN)

            board = Board()
            board.add_peg_at_track_position(red_peg, 0)

            red_start_board_position = board.track_position_to_board_position(0, Color.RED)
            assert red_start_board_position is not None
            green_track_position = board.board_position_to_track_position(red_start_board_position, Color.GREEN) + 1
            board.add_peg_at_track_position(green_peg, green_track_position)

            action = MoveAction(1, Color.RED, board)
            assert action.get_applicable_pegs() == [red_peg]

        def test_should_only_return_unblocked_pegs(self):
            peg1 = Peg(1, Color.RED)
            peg2 = Peg(2, Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg1, 0)
            board.add_peg_at_track_position(peg2, 1)

            action = MoveAction(1, Color.RED, board)
            assert action.get_applicable_pegs() == [peg2]

        def test_should_allow_pegs_in_final_slots_to_move(self):
            peg = Peg(1, Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - 2)

            action = MoveAction(1, Color.RED, board)
            assert action.get_applicable_pegs() == [peg]
            
    class TestApply:
        def test_should_move_peg_to_new_track_position(self):
            peg = Peg(1, Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            action = MoveAction(1, Color.RED, board)
            action.apply(peg)

            assert board.get_track_position_for_peg(peg) == 1

        def test_should_bump_any_peg_in_the_way_to_on_deck(self):
            red_peg = Peg(1, Color.RED)
            green_peg = Peg(2, Color.GREEN)

            board = Board()
            board.add_peg_at_track_position(red_peg, 0)

            red_start_board_position = board.track_position_to_board_position(0, Color.RED)
            assert red_start_board_position is not None
            green_track_position = board.board_position_to_track_position(red_start_board_position, Color.GREEN) + 1
            board.add_peg_at_track_position(green_peg, green_track_position)

            action = MoveAction(1, Color.RED, board)
            action.apply(red_peg)

            assert board.is_peg_on_deck(green_peg) == True
            assert board.get_track_position_for_peg(red_peg) == 1