import numpy
import keras
import tensorflow

from typing import Optional
from numpy.typing import NDArray
from abc import ABC, abstractmethod

class Model(ABC):
    def __init__(self, id: Optional[str]):
        self.id: Optional[str] = id
        self._model: Optional[keras.Model] = None

    @abstractmethod
    def build(self):
        pass

    def fit(self, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]):
        assert self._model is not None
        self._model.fit(X, Y, epochs=10)

    def calculate_accuracy(self, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]) -> float:
        assert self._model is not None
        Y_pred = self._model.predict(X)
        Y_sigmoid = tensorflow.math.sigmoid(Y_pred)
        Y_errors = numpy.where(Y_sigmoid >= 0.5, 1, 0)
        return numpy.mean(Y_errors == Y)
    
    @property
    def model(self):
        return self._model