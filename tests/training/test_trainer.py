import numpy
from numpy.typing import NDArray

from trouble.training import Trainer, Model, EncodedTurnState
from trouble.generation import GameDocument, TurnModel, BoardModel, GameRepository

class MockModel(Model):
    def __init__(self):
        super().__init__(id="MockModel")
        self.X = None
        self.Y = None

    def build(self):
        pass

    def fit(self, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]):
        self.X = X
        self.Y = Y

class TestTrainer:
    class TestTrain:
        async def test_should_provide_training_data_to_fit_the_model(self):
            game_repository = GameRepository()

            for _ in range(4):
                game = GameDocument(
                    winner="red",
                    turns=[
                        TurnModel(
                            color="red",
                            roll=1,
                            color_turns=1,
                            board=BoardModel(
                                red=[1, 2, 3, 4],
                                blue=[1, 2, 3, 4],
                                green=[1, 2, 3, 4],
                                yellow=[1, 2, 3, 4]
                            )
                        )
                    ]
                )
                await game_repository.add(game)

            model = MockModel()

            trainer = Trainer()
            await trainer.train(model)

            # half the data ends up in test set
            assert model.X is not None and model.Y is not None
            assert model.X.shape == (2, EncodedTurnState.SIZE)
            assert model.Y.shape == (2, 1)

            assert trainer.X_test.shape == (2, EncodedTurnState.SIZE)
            assert trainer.Y_test.shape == (2, 1)