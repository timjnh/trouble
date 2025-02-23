import asyncio
from argparse import ArgumentParser
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import List

from trouble import Game, Board, RandomActionSelector, DefaultDie, Color, Peg
from trouble.models import GameDocument, TurnModel, BoardModel

parser = ArgumentParser(description="Generate games of trouble")
parser.add_argument("--persist", action="store_true", help="Persist the game to mongo")
parser.add_argument("--mongo-uri", type=str, default="mongodb://localhost:27017/trouble", help="MongoDB URI")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
args = parser.parse_args()

async def main():
    if args.persist:
        mongo_client = AsyncIOMotorClient(args.mongo_uri)
        await init_beanie(database=mongo_client.db_name, document_models=[GameDocument])

    board = Board()
    for color in Color:
        for _ in range(4):
            board.add_peg(Peg(color))

    action_selector = RandomActionSelector()
    die = DefaultDie()

    game = Game(board, action_selector, die)

    turns: List[TurnModel] = []
    while not game.is_complete:
        color = game.current_color
        game.take_turn()

        assert die.last_roll is not None
        turns.append(TurnModel(
            color=color,
            color_turns=game.current_color_turns,
            board=BoardModel.from_board(board),
            roll=die.last_roll,
        ))

        if args.verbose:
            print(f"\033[97mColor: {game.current_color.to_styled_string()}\033[97m, Turns: {game.current_color_turns}, Roll: {die.last_roll}, Total turns: {len(turns)}")
            print(board)
            print()

    assert game.winner is not None

    if args.persist:
        game_document = GameDocument(turns=turns, winner=game.winner)
        await game_document.insert()

    if args.verbose:
        print(f"\033[97mWinner: {game.winner.to_styled_string()}\033[97m, Total turns: {turns}")

asyncio.run(main())