import random
import asyncio
from argparse import ArgumentParser, Namespace
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import List, Tuple

from trouble import Game, Board, RandomActionSelector, DefaultDie, Color, Peg
from trouble.models import GameDocument, TurnModel, BoardModel
from trouble.repositories import GameRepository
from trouble.training import Trainer, ThreeLayerModel

def play_game() -> Tuple[Game, List[TurnModel]]:
    board = Board()
    for color in Color:
        for i in range(4):
            board.add_peg(Peg((Color.ordinal(color) * 4) + i, color))

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

async def connect_to_mongo(mongo_uri: str, mongo_db):
    mongo_client = AsyncIOMotorClient(mongo_uri)
    await init_beanie(database=mongo_client[mongo_db], document_models=[GameDocument])

async def generate(args: Namespace):
    game_repository = GameRepository()
    
    if args.persist:
        await connect_to_mongo(args.mongo_uri, args.mongo_db)

    for i in range(args.num_games):
        i += 1
        if i % 1000 == 0:
            print(f"Generating game {i} of {args.num_games}...")

        game, turns = play_game()

        if args.persist:
            assert game.winner is not None
            game_document = GameDocument(turns=turns, winner=str(game.winner))

            await game_repository.add(game_document)

async def train(args: Namespace):
    await connect_to_mongo(args.mongo_uri, args.mongo_db)

    model = ThreeLayerModel()
    model.build()

    trainer = Trainer()
    await trainer.train(model)
    print("Training complete!")

parser = ArgumentParser(description="Play, generate and train machine-learning solutions on the game of Trouble")
subparsers = parser.add_subparsers(required=True)

generate_parser = subparsers.add_parser("generate", help="Generate games for use in training")
generate_parser.add_argument("--persist", action="store_true", help="Persist the game to mongo")
generate_parser.add_argument("--mongo-uri", type=str, default="mongodb://localhost:27017/", help="MongoDB URI")
generate_parser.add_argument("--mongo-db", type=str, default="trouble", help="MongoDB database name")
generate_parser.add_argument("--num-games", "-n", type=int, default=1, help="Number of games to generate")
generate_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
generate_parser.set_defaults(call=generate)

train_parser = subparsers.add_parser("train", help="Train a machine-learning model on saved games")
train_parser.add_argument("--mongo-uri", type=str, default="mongodb://localhost:27017/", help="MongoDB URI")
train_parser.add_argument("--mongo-db", type=str, default="trouble", help="MongoDB database name")
train_parser.set_defaults(call=train)

args = parser.parse_args()
asyncio.run(args.call(args))