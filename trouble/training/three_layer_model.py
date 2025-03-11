import numpy
from numpy.typing import NDArray
import tensorflow
import keras
from keras import Sequential, layers, optimizers, losses
from typing import Optional

from .model import Model

class ThreeLayerModel(Model):
    def __init__(self):
        self._model: Optional[keras.Model] = None

    def build(self):
        self._model = Sequential([
            layers.Dense(units=128, activation='relu'),
            layers.Dense(units=25, activation='relu'),
            layers.Dense(units=1, activation='linear')
        ])

        self._model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss=losses.BinaryCrossentropy(from_logits=True),
        )

    def fit(self, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]):
        assert self._model is not None
        self._model.fit(X, Y, epochs=10)

    def calculate_accuracy(self, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]) -> float:
        assert self._model is not None
        Y_pred = self._model.predict(X)
        Y_sigmoid = tensorflow.math.sigmoid(Y_pred)
        Y_errors = numpy.where(Y_sigmoid >= 0.5, 1, 0)
        return numpy.mean(Y_errors == Y)