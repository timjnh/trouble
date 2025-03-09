import numpy

from ..models import GameDocument

class Trainer:
    async def train(self):
        games_count = await GameDocument.count()
        X_train = numpy.zeros((games_count, EncodedGameState.SIZE))

        games = GameDocument.find()
        async for game in games:
            print(game)