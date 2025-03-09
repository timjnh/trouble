import numpy
import tensorflow
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Dense
from tensorflow.python.keras.optimizers import Adam
from tensorflow.python.keras.losses import BinaryCrossentropy

from ..models import GameDocument
from .encoded_turn_state import EncodedTurnState

class Trainer:
    async def train(self):
        model = Sequential([
            Dense(units=128, activation='relu', input_shape=(EncodedTurnState.SIZE,)),
            Dense(units=25, activation='relu'),
            Dense(units=1, activation='sigmoid')
        ])

        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss=BinaryCrossentropy()
        )

        games_count = await GameDocument.count()
        X_train = numpy.zeros((games_count, EncodedTurnState.SIZE))

        games = GameDocument.find()
        async for game in games:
            print(game)