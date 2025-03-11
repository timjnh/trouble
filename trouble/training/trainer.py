import numpy
import tensorflow
from keras import Sequential
from keras import Sequential, layers, optimizers, losses
from sklearn.model_selection import train_test_split

from .. import Color
from ..models import GameDocument
from ..repositories import GameRepository
from .encoded_turn_state import EncodedTurnState
from .model import Model

class Trainer:
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

        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.4)

        model.fit(X_train, Y_train)

        training_accuracy = model.calculate_accuracy(X_train, Y_train)
        test_accuracy = model.calculate_accuracy(X_test, Y_test)

        print(f'Training accuracy: {training_accuracy}')
        print(f'Test accuracy: {test_accuracy}')