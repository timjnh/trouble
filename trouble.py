from trouble import Game, Board, RandomActionSelector, DefaultDie, Color, Peg

board = Board()
for color in Color:
    for _ in range(4):
        board.add_peg(Peg(color))

action_selector = RandomActionSelector()
die = DefaultDie()

game = Game(board, action_selector, die)

while not game.is_complete:
    game.take_turn()

    print(f"\033[97mColor: {game.current_color}\033[97m, Turns: {game.current_color_turns}, Roll: {die.last_roll}")
    print(board)
    print()

print(f"Winner: {game.winner}")