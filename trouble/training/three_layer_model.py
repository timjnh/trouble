from keras import Sequential, layers, optimizers, losses

from .model import Model

class ThreeLayerModel(Model):
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