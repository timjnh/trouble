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
        self.epochs = 10

    @abstractmethod
    def build(self):
        pass

    def fit(self, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]):
        assert self._model is not None
        self._model.fit(X, Y, epochs=self.epochs)

    def calculate_accuracy(self, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]) -> float:
        assert self._model is not None
        Y_sigmoid = self._predict_sigmoid(X)
        Y_pred = numpy.where(Y_sigmoid >= 0.5, 1, 0)
        return float(numpy.mean(Y_pred == Y))
    
    def predict_with_threshold(self, X: NDArray[numpy.int8], threshold: float = 0.5) -> bool:
        return bool(self.predict(X) >= threshold)

    def predict(self, X: NDArray[numpy.int8]) -> numpy.float32:
        assert self._model is not None
        assert len(X.shape) == 1
        Y_sigmoid = self._predict_sigmoid(X.reshape((1, X.shape[0])))
        return Y_sigmoid[0][0]
    
    def _predict_sigmoid(self, X: NDArray[numpy.int8]) -> NDArray[numpy.float32]:
        assert self._model is not None
        Y_pred = self._model.predict(X, verbose="0")
        return tensorflow.math.sigmoid(Y_pred).numpy()
    
    @property
    def model(self):
        return self._model