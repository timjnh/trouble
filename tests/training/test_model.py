import pytest
import numpy
from keras import Sequential, layers, optimizers, losses

from numpy.typing import NDArray

from trouble.training import Model

class SimpleModel(Model):
    def __init__(self, id: str):
        super().__init__(id)
        self.epochs = 10

    def build(self):
        self._model = Sequential([
            layers.Dense(units=25, activation='relu'),
            layers.Dense(units=15, activation='relu'),
            layers.Dense(units=1, activation='linear')
        ])

        self._model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss=losses.BinaryCrossentropy(from_logits=True),
        )

class TestModel:
    @pytest.fixture(scope="class")
    def X(self) -> NDArray[numpy.int8]:
        return numpy.concatenate([
                numpy.array(numpy.zeros((100, 1), dtype=numpy.int8)),
                numpy.array(numpy.ones((100, 1), dtype=numpy.int8))
            ],
            axis=0
        )
    
    @pytest.fixture(scope="class")
    def Y(self) -> NDArray[numpy.int8]:
        return numpy.concat([
                numpy.array(numpy.zeros((100, 1), dtype=numpy.int8)),
                numpy.array(numpy.ones((100, 1), dtype=numpy.int8))
            ],
            axis=0
        )

    @pytest.fixture(scope="class")
    def model(self, X, Y) -> SimpleModel:
        model = SimpleModel(id="test")
        model.build()
        model.fit(X, Y)
        return model

    class TestCalculateAccuracy:
        def test_should_predict_accuracy(self, model: SimpleModel, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]):
            assert model.calculate_accuracy(X, Y) == 1.0

    class TestPredict:
        def test_should_return_the_prediction_for_the_given_input(self, model: SimpleModel, X: NDArray[numpy.int8], Y: NDArray[numpy.int8]):
            prediction = model.predict(X[0])
            assert prediction > 0.0 and prediction < 0.5