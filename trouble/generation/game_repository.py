from beanie.odm.queries.find import FindMany
from beanie.odm.fields import PydanticObjectId

from . import GameDocument

ObjectId = PydanticObjectId

class NoSuchGameError(Exception):
    def __init__(self, id: ObjectId):
        super().__init__(f"No game found with id {id}")

class GameRepository:
    async def add(self, game: GameDocument):
        await game.insert()
    
    def find_all(self) -> FindMany[GameDocument]:
        return GameDocument.find()
    
    async def find_by_id(self, id: ObjectId) -> GameDocument:
        game = await GameDocument.get(id)
        if game is None:
            raise NoSuchGameError(id)
        return game
    
    async def total_turns(self) -> int:
        pipeline = [
            { "$unwind": { "path": "$turns" } },
            { "$count": "total_turns" }
        ]

        result = await GameDocument.aggregate(pipeline).to_list()

        return result[0]["total_turns"]