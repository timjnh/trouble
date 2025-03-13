import os
import keras
from keras import models
from glob import glob

from typing import Type, cast

from trouble.training import Model, ThreeLayerModel

class NoSuchModelError(Exception):
    def __init__(self, id: str):
        super().__init__(f"No such model with id: {id}")

class ModelRepository:
    def save(self, model: Model):
        assert model.model and model.id

        model_directory = self._directory_for_id(model.id)
        if not os.path.exists(model_directory):
            os.makedirs(model_directory)
        model.model.save(self._path_for_id_and_model_type(model.id, type(model)))

    def find_by_id(self, id: str) -> Model:
        model_type = self._get_model_type_for_id(id)
        keras_model = models.load_model(self._path_for_id_and_model_type(id, model_type))
        if keras_model is None:
            raise NoSuchModelError(id)
        
        model = model_type(id)
        model._model = cast(keras.Model, keras_model)
        return model
    
    def delete(self, id: str):
        model_directory = self._directory_for_id(id)
        if os.path.exists(model_directory):
            for file in glob(f"{model_directory}/*.keras"):
                os.remove(file)
            os.rmdir(model_directory)

    def _get_model_type_for_id(self, id: str) -> Type[Model]:
        keras_files = glob(f"{self._directory_for_id(id)}/*.keras")
        if len(keras_files) == 0:
            raise NoSuchModelError(id)
        elif len(keras_files) > 1:
            raise Exception(f"Multiple models found for id: {id}")
        
        model_type = keras_files[0].split('/')[-1].split('.')[0]
        return globals()[model_type]

    def _path_for_id_and_model_type(self, id: str, model_type: Type[Model]) -> str:
        return f"{self._directory_for_id(id)}/{model_type.__name__}.keras"
    
    def _directory_for_id(self, id: str) -> str:
        return f"models/{id}/"