from trouble import Board, Peg, Color

class TestBoard:
    class TestReset:
        def test_moves_all_pegs_to_on_deck(self):
            red_peg = Peg(Color.RED)
            red_peg.position = 0

            green_peg_1 = Peg(Color.GREEN)
            green_peg_1.position = 3

            green_peg_2 = Peg(Color.GREEN)

            board = Board()
            board.add_pegs([red_peg, green_peg_1, green_peg_2])

            assert len(board.pegs) == 3
            assert len(board.get_pegs_on_deck(Color.GREEN)) == 1
            assert len(board.get_pegs_on_deck(Color.RED)) == 0

            board.reset()

            assert len(board.pegs) == 3
            assert len(board.get_pegs_on_deck(Color.GREEN)) == 2
            assert len(board.get_pegs_on_deck(Color.RED)) == 1

    class TestAddPegs:
        def test_adds_pegs_to_board(self):
            red_peg = Peg(Color.RED)
            green_peg = Peg(Color.GREEN)

            board = Board()
            board.add_pegs([red_peg, green_peg])

            assert len(board.pegs) == 2
            assert len(board.get_pegs_on_deck(Color.RED)) == 1
            assert len(board.get_pegs_on_deck(Color.GREEN)) == 1

    class TestGetPegsOnBoard:
        def test_returns_all_pegs_on_board(self):
            red_peg_on_board = Peg(Color.RED)
            red_peg_on_board.position = 0

            red_peg_on_deck = Peg(Color.RED)

            red_peg_in_final_slot = Peg(Color.RED)
            red_peg_in_final_slot.position = Board.FULL_TRACK_LENGTH - 1

            board = Board()
            board.add_pegs([red_peg_on_board, red_peg_on_deck, red_peg_in_final_slot])

            assert len(board.get_pegs_on_board(Color.RED)) == 1

    class TestGetPegsOnDeck:
        def test_returns_all_pegs_on_deck(self):
            red_peg_on_deck = Peg(Color.RED)

            red_peg_on_board = Peg(Color.RED)
            red_peg_on_board.position = 0

            red_peg_in_final_slot = Peg(Color.RED)
            red_peg_in_final_slot.position = Board.FULL_TRACK_LENGTH - 1

            board = Board()
            board.add_pegs([red_peg_on_board, red_peg_on_deck, red_peg_in_final_slot])

            assert len(board.get_pegs_on_deck(Color.RED)) == 1

    class TestGetPegsInFinalSlots:
        def test_returns_pegs_in_final_slots_matching_given_color(self):
            red_peg_1 = Peg(Color.RED)
            red_peg_1.position = 0

            red_peg_2 = Peg(Color.RED)
            red_peg_2.position = Board.FULL_TRACK_LENGTH - 1

            green_peg = Peg(Color.GREEN)
            green_peg.position = Board.FULL_TRACK_LENGTH - 1

            board = Board()
            board.add_pegs([red_peg_1, red_peg_2, green_peg])

            assert len(board.get_pegs_in_final_slots(Color.RED)) == 1
            assert len(board.get_pegs_in_final_slots(Color.GREEN)) == 1

        def test_returns_an_empty_list_with_no_pegs_of_color_added_to_board(self):
            board = Board()

            assert len(board.get_pegs_in_final_slots(Color.BLUE)) == 0

        def test_returns_an_empty_list_with_no_pegs_of_given_color_in_final_slots(self):
            red_peg = Peg(Color.RED)
            red_peg.position = 0

            board = Board()
            board.add_pegs([red_peg])

            assert len(board.get_pegs_in_final_slots(Color.RED)) == 0

        def test_returns_an_empty_list_with_all_pegs_of_given_color_on_deck(self):
            board = Board()
            board.add_pegs([Peg(Color.RED)])

            assert len(board.get_pegs_in_final_slots(Color.RED)) == 0

    class TestGetBoardPegPosition:
        def test_returns_none_if_peg_is_on_deck(self):
            peg = Peg(Color.RED)
            assert peg.is_on_deck == True

            board = Board()
            board.add_pegs([peg])

            assert board.get_board_peg_position(peg) is None

        def test_returns_none_if_the_peg_is_in_final_slots(self):
            peg = Peg(Color.RED)
            peg.position = Board.FULL_TRACK_LENGTH - 1

            board = Board()
            board.add_pegs([peg])

            assert board.get_board_peg_position(peg) is None

        def test_returns_the_peg_position_plus_the_color_offset(self):
            red_peg = Peg(Color.RED)
            red_peg.position = 0

            green_peg_1 = Peg(Color.GREEN)
            green_peg_1.position = 0

            green_peg_2 = Peg(Color.GREEN)
            green_peg_2.position = 3

            board = Board()
            board.add_pegs([red_peg, green_peg_1, green_peg_2])

            # red offset is 0
            assert board.get_board_peg_position(red_peg) == 0

            # green offset is 7
            assert board.get_board_peg_position(green_peg_1) == 7
            assert board.get_board_peg_position(green_peg_2) == 10

        def test_loops_at_around_at_end_of_track(self):
            peg = Peg(Color.BLUE)
            peg.position = 7

            board = Board()
            board.add_pegs([peg])

            assert board.get_board_peg_position(peg) == 0

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
            peg.position = 0

            board = Board()
            board.add_pegs([peg])

            assert board.get_peg_at_board_position(1) is None

        def test_returns_the_peg_at_the_board_position(self):
            peg = Peg(Color.GREEN)
            peg.position = 0

            board = Board()
            board.add_pegs([peg])

            assert board.get_peg_at_board_position(7) == peg