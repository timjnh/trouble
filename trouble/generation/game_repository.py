from typing import Any, Coroutine

from . import GameDocument

class GameRepository:
    def add(self, game: GameDocument) -> Coroutine[Any, Any, GameDocument]:
        return game.insert()
    
    async def total_turns(self) -> int:
        pipeline = [
            { "$unwind": { "path": "$turns" } },
            { "$count": "total_turns" }
        ]

        result = await GameDocument.aggregate(pipeline).to_list()

        return result[0]["total_turns"]