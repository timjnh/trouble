import numpy
from keras import Sequential, layers, optimizers, losses

from trouble.training import Model

class SimpleModel(Model):
    def __init__(self, id: str):
        super().__init__(id)
        self.epochs = 3

    def build(self):
        self._model = Sequential([
            layers.Dense(units=4, activation='relu'),
            layers.Dense(units=1, activation='linear')
        ])

        self._model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss=losses.BinaryCrossentropy(from_logits=True),
        )

class TestModel:
    class TestCalculateAccuracy:
        def test_should_predict_accuracy(self):
            model = SimpleModel(id="test")
            model.build()

            X = numpy.array([[0], [1]])
            Y = numpy.array([[0], [1]])
            model.fit(X, Y)

            accuracy = model.calculate_accuracy(X, Y)
            assert accuracy == 1.0