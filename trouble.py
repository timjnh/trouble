from argparse import ArgumentParser

from trouble import Game, Board, RandomActionSelector, DefaultDie, Color, Peg

parser = ArgumentParser(description="Generate games of trouble")
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
args = parser.parse_args()

board = Board()
for color in Color:
    for _ in range(4):
        board.add_peg(Peg(color))

action_selector = RandomActionSelector()
die = DefaultDie()

game = Game(board, action_selector, die)

turns = 0
while not game.is_complete:
    game.take_turn()
    turns += 1

    if args.verbose:
        print(f"\033[97mColor: {game.current_color}\033[97m, Turns: {game.current_color_turns}, Roll: {die.last_roll}, Total turns: {turns}")
        print(board)
        print()

if args.verbose:
    print(f"\033[97mWinner: {game.winner}\033[97m, Total turns: {turns}")