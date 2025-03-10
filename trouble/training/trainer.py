import numpy
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import BinaryCrossentropy
from typing import Coroutine, Any

from .. import Color
from ..models import GameDocument
from ..repositories import GameRepository
from .encoded_turn_state import EncodedTurnState

class Trainer:
    async def train(self):
        game_repository = GameRepository()
        turns_count = await game_repository.total_turns()
        X_train = numpy.zeros((turns_count, EncodedTurnState.SIZE))
        Y_train = numpy.zeros((turns_count, 1))

        games = GameDocument.find()
        i = 0
        async for game in games:
            i += 1
            for i, turn in enumerate(game.turns):
                X_train[i] = EncodedTurnState.encode(turn)
                Y_train[i] = game.winner == str(Color.RED)

        model = Sequential([
            Dense(units=128, activation='relu'),#, input_shape=(EncodedTurnState.SIZE,)),
            Dense(units=25, activation='relu'),
            Dense(units=1, activation='sigmoid')
        ])

        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss=BinaryCrossentropy()
        )

        model.fit(X_train, Y_train, epochs=10)