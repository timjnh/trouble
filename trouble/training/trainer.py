import numpy
from sklearn.model_selection import train_test_split

from numpy.typing import NDArray
from typing import Optional

from ..gameplay import Color
from ..generation import GameDocument, GameRepository
from .encoded_turn_state import EncodedTurnState
from .model import Model

class Trainer:
    def __init__(self):
        self._X_train: Optional[NDArray[numpy.int8]] = None
        self._Y_train: Optional[NDArray[numpy.int8]] = None
        self._X_test: Optional[NDArray[numpy.int8]] = None
        self._Y_test: Optional[NDArray[numpy.int8]] = None

    async def train(self, model: Model):
        game_repository = GameRepository()
        turns_count = await game_repository.total_turns()
        X = numpy.zeros((turns_count, EncodedTurnState.SIZE))
        Y = numpy.zeros((turns_count, 1))

        games = GameDocument.find()
        i = 0
        async for game in games:
            for turn in game.turns:
                X[i] = EncodedTurnState.encode(turn)
                Y[i] = game.winner == str(Color.RED)
                i += 1

        self._X_train, self._X_test, self._Y_train, self._Y_test = train_test_split(X, Y, test_size=0.4)
        assert self._X_train is not None and self._Y_train is not None

        model.fit(self._X_train, self._Y_train)

    @property
    def X_train(self) -> NDArray[numpy.int8]:
        assert self._X_train is not None
        return self._X_train
    
    @property
    def Y_train(self) -> NDArray[numpy.int8]:
        assert self._Y_train is not None
        return self._Y_train
    
    @property
    def X_test(self) -> NDArray[numpy.int8]:
        assert self._X_test is not None
        return self._X_test
    
    @property
    def Y_test(self) -> NDArray[numpy.int8]:
        assert self._Y_test is not None
        return self._Y_test