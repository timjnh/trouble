import random
import asyncio
from argparse import ArgumentParser
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import List, Tuple

from trouble import Game, Board, RandomActionSelector, DefaultDie, Color, Peg
from trouble.models import GameDocument, TurnModel, BoardModel

parser = ArgumentParser(description="Generate games of trouble")
parser.add_argument("--persist", action="store_true", help="Persist the game to mongo")
parser.add_argument("--mongo-uri", type=str, default="mongodb://localhost:27017/", help="MongoDB URI")
parser.add_argument("--mongo-db", type=str, default="trouble", help="MongoDB database name")
parser.add_argument("--num-games", "-n", type=int, default=1, help="Number of games to generate")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
args = parser.parse_args()

def play_game() -> Tuple[Game, List[TurnModel]]:
    board = Board()
    for color in Color:
        for i in range(4):
            board.add_peg(Peg((i * Color.ordinal(color)) + 1, color))

    action_selector = RandomActionSelector()
    die = DefaultDie()

    game = Game(board, action_selector, die, random.choice(list(Color)))

    turns: List[TurnModel] = []
    while not game.is_complete:
        color = game.current_color
        color_turns = game.current_color_turns
        game.take_turn()

        assert die.last_roll is not None
        turns.append(TurnModel(
            color=str(color),
            color_turns=color_turns,
            board=BoardModel.from_board(board),
            roll=die.last_roll,
        ))

        if args.verbose:
            print(f"\033[97mColor: {game.current_color.to_styled_string()}\033[97m, Turns: {game.current_color_turns}, Roll: {die.last_roll}, Total turns: {len(turns)}")
            print(board)
            print()

    assert game.winner is not None
    if args.verbose:
        print(f"\033[97mWinner: {game.winner.to_styled_string()}\033[97m, Total turns: {len(turns)}")

    return game, turns

async def main():
    if args.persist:
        mongo_client = AsyncIOMotorClient(args.mongo_uri)
        await init_beanie(database=mongo_client[args.mongo_db], document_models=[GameDocument])

    for i in range(args.num_games):
        i += 1
        if i % 1000 == 0:
            print(f"Generating game {i} of {args.num_games}...")

        game, turns = play_game()

        if args.persist:
            assert game.winner is not None
            game_document = GameDocument(turns=turns, winner=str(game.winner))
            await game_document.insert()

asyncio.run(main())