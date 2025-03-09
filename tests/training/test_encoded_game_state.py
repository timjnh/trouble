from trouble.models import GameDocument, TurnModel, BoardModel
from . import EncodedGameState

class TestEncodedGameState:
    class TestEncode:
        def test_should_return_number_of_turns_followed_by_all_board_positions(self):
            board = BoardModel(
                on_deck=["R", "R", "G", "G", "B", "B", "B"],
                color_by_board_position={
                    0: "R",
                    10: "G",
                    11: "Y"
                },
                final_slots=["B", "Y", "G", "R", "Y", "Y"]
            )

            turn = TurnModel(
                color="R",
                color_turns=2,
                board=board,
                roll=6
            )

            game = GameDocument(
                turns=[turn],
                winner="R"
            )

            encoded = EncodedGameState.encode(game)

            assert encoded == [2, 33, ]