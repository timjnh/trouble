from trouble.training import Model

class ModelRepository:
    def save(self, model: Model):
        assert model.model and model.id
        model.model.save(f"models/{model.id}.keras")