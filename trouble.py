import random
import asyncio
from argparse import ArgumentParser, Namespace
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from typing import List, Tuple

from trouble.gameplay import Game, Board, RandomActionSelector, DefaultDie, Color, Peg, ActionSelector
from trouble.generation import GameDocument, TurnModel, BoardModel, GameRepository
from trouble.training import ModelRepository, Trainer, ThreeLayerModel
from trouble.evaluation import GameStateRepository, ModelBasedActionSelector

def play_game(action_selectors: dict[Color, ActionSelector]) -> Tuple[Game, List[TurnModel]]:
    board = Board()
    for color in Color:
        for i in range(4):
            board.add_peg(Peg((Color.ordinal(color) * 4) + i, color))

    die = DefaultDie()
    game = Game(board, action_selectors, die, random.choice(list(Color)))

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

    action_selectors: dict[Color, ActionSelector] = {
        Color.RED: RandomActionSelector(),
        Color.GREEN: RandomActionSelector(),
        Color.BLUE: RandomActionSelector(),
        Color.YELLOW: RandomActionSelector(),
    }
    if args.red_model_id is not None:
        model = ModelRepository().find_by_id(args.red_model_id)
        action_selectors[Color.RED] = ModelBasedActionSelector(model)

    win_counts = {color: 0 for color in Color}
    for i in range(args.num_games):
        i += 1
        if i % 10 == 0:
            print(f"Generating game {i} of {args.num_games}...")

        game, turns = play_game(action_selectors)

        assert game.winner is not None
        win_counts[game.winner] += 1

        if args.persist:
            game_document = GameDocument(turns=turns, winner=str(game.winner))

            await game_repository.add(game_document)

    print(f"Game generation complete! Win counts:")
    for color, count in win_counts.items():
        print(f"  {color.to_styled_string()}: {count} ({round(count / args.num_games * 100, 2)}%)")

async def train(args: Namespace):
    await connect_to_mongo(args.mongo_uri, args.mongo_db)

    model = ThreeLayerModel(args.name or f"3_layer_model_{random.randint(0, 100000)}")
    model.build()

    trainer = Trainer()
    await trainer.train(model)

    training_accuracy = model.calculate_accuracy(trainer.X_train, trainer.Y_train)
    test_accuracy = model.calculate_accuracy(trainer.X_test, trainer.Y_test)

    print(f'Training accuracy: {training_accuracy}')
    print(f'Test accuracy: {test_accuracy}')

    if args.persist:
        ModelRepository().save(model)

    print("Training complete!")

async def evaluate(args: Namespace):
    game_state = GameStateRepository().find_by_path(args.path)
    model = ModelRepository().find_by_id(args.model_id)
    
    selector = ModelBasedActionSelector(model)
    actions = selector.evaluate_possible_actions(game_state.color, game_state.board, game_state.roll, game_state.color_turns)

    print(f"{game_state.board}\n")

    print(f"Color: {game_state.color}, Turns: {game_state.color_turns}, Roll: {game_state.roll}")
    print("Possible Actions:")
    for action in actions:
        print(f"  {action}")
        print(f"    {str(action.board).replace('\n', '\n    ')}")

parser = ArgumentParser(description="Play, generate and train machine-learning solutions on the game of Trouble")
subparsers = parser.add_subparsers(required=True)

generate_parser = subparsers.add_parser("generate", help="Generate games for use in training")
generate_parser.add_argument("--persist", action="store_true", help="Persist the game to mongo")
generate_parser.add_argument("--mongo-uri", type=str, default="mongodb://localhost:27017/", help="MongoDB URI")
generate_parser.add_argument("--mongo-db", type=str, default="trouble", help="MongoDB database name")
generate_parser.add_argument("--num-games", "-n", type=int, default=1, help="Number of games to generate")
generate_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
generate_parser.add_argument("--red-model-id", type=str, help="ID of the model to use for the red player. If not provided, a random action selector will be used.")
generate_parser.set_defaults(call=generate)

train_parser = subparsers.add_parser("train", help="Train a machine-learning model on saved games")
train_parser.add_argument("--mongo-uri", type=str, default="mongodb://localhost:27017/", help="MongoDB URI")
train_parser.add_argument("--mongo-db", type=str, default="trouble", help="MongoDB database name")
train_parser.add_argument("--persist", action="store_true", help="Persist the model to disk")
train_parser.add_argument("--model-id", type=str, help="ID to use when saving the model. If not provided a random name will be generated. Only valid with --persist.")
train_parser.set_defaults(call=train)

evaluate_parser = subparsers.add_parser("evaluate", help="Evaluate a sample game state using a trained model")
evaluate_parser.add_argument("path", type=str, help="Path to the game state to evaluate. See ./sample_game_states")
evaluate_parser.add_argument("--model-id", type=str, default="3_layer_model", help="ID of the model to use for evaluation")
evaluate_parser.set_defaults(call=evaluate)

args = parser.parse_args()
asyncio.run(args.call(args))