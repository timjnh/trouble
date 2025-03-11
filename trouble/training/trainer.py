import numpy
import tensorflow
from keras import Sequential
from keras import Sequential, layers, optimizers, losses
from sklearn.model_selection import train_test_split

from .. import Color
from ..models import GameDocument
from ..repositories import GameRepository
from .encoded_turn_state import EncodedTurnState

class Trainer:
    async def train(self):
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

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4)

        model = Sequential([
            layers.Dense(units=128, activation='relu'),#, input_shape=(EncodedTurnState.SIZE,)),
            layers.Dense(units=25, activation='relu'),
            layers.Dense(units=1, activation='linear')
        ])

        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss=losses.BinaryCrossentropy(from_logits=True),
        )

        model.fit(X_train, Y_train, epochs=10)

        training_accuracy = self._calculate_accuracy(model, X_train, Y_train)
        test_accuracy = self._calculate_accuracy(model, X_test, Y_test)

        print(f'Training accuracy: {training_accuracy}')
        print(f'Test accuracy: {test_accuracy}')

    def _calculate_accuracy(self, model, X, Y) -> float:
        Y_pred = model.predict(X)
        Y_sigmoid = tensorflow.math.sigmoid(Y_pred)
        Y_errors = numpy.where(Y_sigmoid >= 0.5, 1, 0)
        return numpy.mean(Y_errors == Y)