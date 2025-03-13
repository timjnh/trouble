import pytest

from trouble.training import ThreeLayerModel, ModelRepository, NoSuchModelError

class TestModelRepository:
    class TestSaveAndFind:
        def test_should_save_a_model_and_reload_it(self):
            repository = ModelRepository()

            id = "test_model"
            model = ThreeLayerModel(id)
            model.build()

            repository.save(model)

            found_model = repository.find_by_id(id)

            assert isinstance(found_model, ThreeLayerModel)

            repository.delete(id)

            with pytest.raises(NoSuchModelError):
                repository.find_by_id(id)