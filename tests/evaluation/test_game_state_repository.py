from trouble.gameplay import Color
from trouble.evaluation import GameStateRepository

class TestGameStateRepository:
    class TestFindById:
        def test_builds_the_game_state_from_a_file_on_disk(self):
            repository = GameStateRepository()

            game_state = repository.find_by_path("tests/evaluation/test_game_state.json")

            assert game_state.color == Color.RED
            assert game_state.color_turns == 1
            assert game_state.roll == 6
            assert len(game_state.board.pegs) == 16

            red_peg_1 = game_state.board.get_pegs_by_color(Color.RED)[0]
            assert game_state.board.get_track_position_for_peg(red_peg_1)
                                                               
            red_peg_2 = game_state.board.get_pegs_by_color(Color.RED)[1]
            assert game_state.board.is_peg_on_deck(red_peg_2) is True