from trouble import Board, Peg, Color

class TestBoard:
    class TestReset:
        def test_moves_all_pegs_to_on_deck(self):
            red_peg = Peg(Color.RED)
            green_peg_1 = Peg(Color.GREEN)
            green_peg_2 = Peg(Color.GREEN)

            board = Board()
            board.add_peg_at_track_position(red_peg, 0)
            board.add_peg_at_track_position(green_peg_1, 3)
            board.add_peg(green_peg_2)

            assert len(board.pegs) == 3
            assert len(board.get_pegs_on_deck(Color.GREEN)) == 1
            assert len(board.get_pegs_on_deck(Color.RED)) == 0

            board.reset()

            assert len(board.pegs) == 3
            assert len(board.get_pegs_on_deck(Color.GREEN)) == 2
            assert len(board.get_pegs_on_deck(Color.RED)) == 1

    class TestAddPeg:
        def test_adds_pegs_to_board(self):
            red_peg = Peg(Color.RED)
            green_peg = Peg(Color.GREEN)

            board = Board()
            board.add_peg(red_peg)
            board.add_peg(green_peg)

            assert len(board.pegs) == 2
            assert len(board.get_pegs_on_deck(Color.RED)) == 1
            assert len(board.get_pegs_on_deck(Color.GREEN)) == 1

    class TestAddPegAtTrackPosition:
        def test_adds_pegs_to_board_at_track_position(self):
            red_peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, 1)

            assert len(board.pegs) == 1
            assert len(board.get_pegs_on_deck(Color.RED)) == 0
            assert board.get_track_position_for_peg(red_peg) == 1

    class TestSetPegTrackPosition:
        def test_sets_the_position_of_an_on_deck_peg(self):
            red_peg = Peg(Color.RED)

            board = Board()
            board.add_peg(red_peg)
            assert board.is_peg_on_deck(red_peg) is True

            board.set_peg_track_position(red_peg, 1)
            new_board_position = board.track_position_to_board_position(1, Color.RED)
            assert new_board_position is not None and board.get_peg_at_board_position(new_board_position) == red_peg
            assert board.is_peg_on_deck(red_peg) is False
        
        def test_sets_the_position_of_a_peg_on_the_board(self):
            red_peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, 1)
            assert board.is_peg_on_deck(red_peg) is False

            board.set_peg_track_position(red_peg, 2)
            old_board_position = board.track_position_to_board_position(1, Color.RED)
            new_board_position = board.track_position_to_board_position(2, Color.RED)
            
            assert new_board_position is not None and board.get_peg_at_board_position(new_board_position) == red_peg
            assert old_board_position is not None and board.get_peg_at_board_position(old_board_position) is None
            assert board.is_peg_on_deck(red_peg) is False

        def test_can_move_pegs_into_final_slots(self):
            red_peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, 1)
            assert board.is_peg_on_deck(red_peg) is False
            assert board.board_position_by_peg[red_peg.id] is not None

            final_slot_position = Board.FULL_TRACK_LENGTH - 1
            board.set_peg_track_position(red_peg, final_slot_position)

            assert board.board_position_by_peg.get(red_peg.id) is None

            old_board_position = board.track_position_to_board_position(1, Color.RED)
            assert old_board_position is not None and board.get_peg_at_board_position(old_board_position) is None
            assert board.get_peg_at_track_position(1, Color.RED) is None

            assert board.is_peg_on_deck(red_peg) is False
            assert board.is_peg_in_final_slots(red_peg) is True

        def test_can_move_pegs_within_final_slots(self):
            red_peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, Board.FULL_TRACK_LENGTH - 2)
            assert board.is_peg_on_deck(red_peg) is False

            board.set_peg_track_position(red_peg, Board.FULL_TRACK_LENGTH - 1)

            assert board.get_peg_at_track_position(Board.FULL_TRACK_LENGTH - 2, Color.RED) is None

    class TestSetPegOnDeck:
        def test_moves_peg_from_on_board_to_deck(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)
            assert board.is_peg_on_deck(peg) is False

            board.set_peg_on_deck(peg)

            assert len(board.pegs) == 1
            assert len(board.get_pegs_on_deck(Color.RED)) == 1
            assert board.get_board_position_for_peg(peg) is None
            assert board.is_peg_on_deck(peg) is True

        def test_moves_peg_from_final_slot_to_on_deck(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - 1)
            assert board.is_peg_in_final_slots(peg) is True

            board.set_peg_on_deck(peg)

            assert len(board.pegs) == 1
            assert len(board.get_pegs_on_deck(Color.RED)) == 1
            assert board.is_peg_in_final_slots(peg) is False

    class TestIsPegOnDeck:
        def test_returns_true_if_peg_is_on_deck(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            assert board.is_peg_on_deck(peg) is True

        def test_returns_false_if_peg_is_on_board(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            assert board.is_peg_on_deck(peg) is False

        def test_returns_false_if_peg_is_in_final_slots(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - 1)

            assert board.is_peg_on_deck(peg) is False

    class TestGetPegsByColor:
        def test_returns_all_pegs_of_color(self):
            red_peg = Peg(Color.RED)
            green_peg = Peg(Color.GREEN)

            board = Board()
            board.add_peg(red_peg)
            board.add_peg(green_peg)

            assert len(board.get_pegs_by_color(Color.RED)) == 1
            assert len(board.get_pegs_by_color(Color.GREEN)) == 1

    class TestGetPegsOnBoard:
        def test_returns_pegs_on_board_on_color(self):
            red_peg_on_board = Peg(Color.RED)
            red_peg_on_deck = Peg(Color.RED)
            red_peg_in_final_slot = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg_on_board, 0)
            board.add_peg(red_peg_on_deck)
            board.add_peg_at_track_position(red_peg_in_final_slot, Board.FULL_TRACK_LENGTH - 1)

            assert len(board.get_pegs_on_board(Color.RED)) == 1

        def test_returns_all_pegs_on_board(self):
            assert False

    class TestGetPegsOnDeck:
        def test_returns_all_pegs_on_deck(self):
            red_peg_on_deck = Peg(Color.RED)
            red_peg_on_board = Peg(Color.RED)
            red_peg_in_final_slot = Peg(Color.RED)

            board = Board()
            board.add_peg(red_peg_on_deck)
            board.add_peg_at_track_position(red_peg_on_board, 0)
            board.add_peg_at_track_position(red_peg_in_final_slot, Board.FULL_TRACK_LENGTH - 1)

            assert len(board.get_pegs_on_deck(Color.RED)) == 1

    class TestGetPegsInFinalSlots:
        def test_returns_pegs_in_final_slots_matching_given_color(self):
            red_peg_1 = Peg(Color.RED)
            red_peg_2 = Peg(Color.RED)
            green_peg = Peg(Color.GREEN)

            board = Board()
            board.add_peg_at_track_position(red_peg_1, 0)
            board.add_peg_at_track_position(red_peg_2, Board.FULL_TRACK_LENGTH - 1)
            board.add_peg_at_track_position(green_peg, Board.FULL_TRACK_LENGTH - 1)

            assert len(board.get_pegs_in_final_slots(Color.RED)) == 1
            assert len(board.get_pegs_in_final_slots(Color.GREEN)) == 1

        def test_returns_an_empty_list_with_no_pegs_of_color_added_to_board(self):
            board = Board()

            assert len(board.get_pegs_in_final_slots(Color.BLUE)) == 0

        def test_returns_an_empty_list_with_no_pegs_of_given_color_in_final_slots(self):
            red_peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(red_peg, 0)

            assert len(board.get_pegs_in_final_slots(Color.RED)) == 0

        def test_returns_an_empty_list_with_all_pegs_of_given_color_on_deck(self):
            board = Board()
            board.add_peg(Peg(Color.RED))

            assert len(board.get_pegs_in_final_slots(Color.RED)) == 0

    class TestIsPegInFinalSlots:
        def test_on_deck_pegs_are_not_in_final_slots(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            assert board.is_peg_in_final_slots(peg) is False

        def test_pegs_on_board_are_not_in_final_slots(self):
            peg = Peg(Color.RED)
            board = Board()
            board.add_peg_at_track_position(peg, 0)
            assert board.is_peg_in_final_slots(peg) is False
    
        def test_pegs_in_final_slots_are_in_final_slots(self):
            peg = Peg(Color.RED)
            board = Board()
            board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - 1)
            assert board.is_peg_in_final_slots(peg) is True

    class TestGetPegBoardPosition:
        def test_returns_none_if_peg_is_on_deck(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            assert board.get_board_position_for_peg(peg) is None

        def test_returns_none_if_the_peg_is_in_final_slots(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, Board.FULL_TRACK_LENGTH - 1)

            assert board.get_board_position_for_peg(peg) is None

        def test_returns_the_peg_position_plus_the_color_offset(self):
            red_peg = Peg(Color.RED)
            green_peg_1 = Peg(Color.GREEN)
            green_peg_2 = Peg(Color.GREEN)

            board = Board()
            board.add_peg_at_track_position(red_peg, 0)
            board.add_peg_at_track_position(green_peg_1, 0)
            board.add_peg_at_track_position(green_peg_2, 3)

            # red offset is 0
            assert board.get_board_position_for_peg(red_peg) == 0

            # green offset is 7
            assert board.get_board_position_for_peg(green_peg_1) == 7
            assert board.get_board_position_for_peg(green_peg_2) == 10

        def test_loops_at_around_at_end_of_track(self):
            peg = Peg(Color.BLUE)

            board = Board()
            board.add_peg_at_track_position(peg, 7)

            assert board.get_board_position_for_peg(peg) == 0

    class TestTrackPositionToBoardPosition:
        def test_returns_the_board_position_for_the_given_track_position_and_color(self):
            board = Board()

            assert board.track_position_to_board_position(0, Color.RED) == 0
            assert board.track_position_to_board_position(0, Color.GREEN) == 7
            assert board.track_position_to_board_position(0, Color.YELLOW) == 14
            assert board.track_position_to_board_position(0, Color.BLUE) == 21

            assert board.track_position_to_board_position(27, Color.RED) == 27
            assert board.track_position_to_board_position(27, Color.GREEN) == 6
            assert board.track_position_to_board_position(27, Color.YELLOW) == 13
            assert board.track_position_to_board_position(27, Color.BLUE) == 20

    class TestBoardPositionToTrackPosition:
        def test_returns_the_track_position_for_the_given_board_position_and_color(self):
            board = Board()

            assert board.board_position_to_track_position(0, Color.RED) == 0
            assert board.board_position_to_track_position(7, Color.GREEN) == 0
            assert board.board_position_to_track_position(14, Color.YELLOW) == 0
            assert board.board_position_to_track_position(21, Color.BLUE) == 0

            assert board.board_position_to_track_position(27, Color.RED) == 27
            assert board.board_position_to_track_position(6, Color.GREEN) == 27
            assert board.board_position_to_track_position(13, Color.YELLOW) == 27
            assert board.board_position_to_track_position(20, Color.BLUE) == 27

    class TestGetPegAtBoardPosition:
        def test_returns_none_if_no_peg_at_board_position(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            assert board.get_peg_at_board_position(1) is None

        def test_returns_the_peg_at_the_board_position(self):
            peg = Peg(Color.GREEN)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            assert board.get_peg_at_board_position(7) == peg

    class TestGetPegAtTrackPosition:
        def test_returns_none_if_no_peg_at_track_position(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            assert board.get_peg_at_track_position(1, Color.RED) is None

        def test_returns_the_peg_at_the_track_position(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg_at_track_position(peg, 0)

            assert board.get_peg_at_track_position(0, Color.RED) == peg

    class TestGetTrackPositionForPeg:
        def test_returns_none_if_peg_is_on_deck(self):
            peg = Peg(Color.RED)

            board = Board()
            board.add_peg(peg)

            assert board.get_track_position_for_peg(peg) is None

        def test_returns_the_track_position_for_the_given_peg(self):
            peg = Peg(Color.GREEN)

            board = Board()
            board.add_peg_at_track_position(peg, 1)

            assert board.get_track_position_for_peg(peg) == 1