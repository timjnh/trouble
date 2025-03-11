import numpy
from numpy.typing import NDArray
from abc import ABC, abstractmethod

class Model(ABC):
    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def fit(self, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]):
        pass

    @abstractmethod
    def calculate_accuracy(self, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]) -> float:
        pass