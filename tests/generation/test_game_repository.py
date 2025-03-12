from trouble.generation import GameDocument, TurnModel, BoardModel, GameRepository

class TestGameRepository:
    class TestTotalTurns:
        async def test_should_return_total_turns_across_all_games(self):
            repository = GameRepository()

            game_1 = GameDocument(
                winner="red",
                turns=[
                    TurnModel(
                        color="red",
                        roll=1,
                        color_turns=1,
                        board=BoardModel(red=[], blue=[], green=[], yellow=[])
                    )
                ]
            )

            game_2 = GameDocument(
                winner="green",
                turns=[
                    TurnModel(
                        color="green",
                        roll=6,
                        color_turns=1,
                        board=BoardModel(red=[], blue=[], green=[], yellow=[])
                    )
                ]
            )

            await repository.add(game_1)
            await repository.add(game_2)

            total_turns = await repository.total_turns()

            assert total_turns == 2