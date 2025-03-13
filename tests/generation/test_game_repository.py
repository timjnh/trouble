import pytest

from trouble.generation import GameDocument, TurnModel, BoardModel, GameRepository, NoSuchGameError, ObjectId

class TestGameRepository:
    class TestFindById:
        async def test_should_return_game_with_matching_id(self):
            repository = GameRepository()

            game = GameDocument(
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

            await repository.add(game)

            assert game.id
            found_game = await repository.find_by_id(game.id)

            assert found_game.id == game.id

        async def test_should_raise_exception_when_no_game_with_matching_id(self):
            repository = GameRepository()

            with pytest.raises(NoSuchGameError):
                await repository.find_by_id(ObjectId("123456789012345678901234"))

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