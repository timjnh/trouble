import json
from dataclasses import dataclass

from trouble.gameplay import Board, Color, Peg

@dataclass
class GameState:
    color: Color
    color_turns: int
    board: Board
    roll: int

class GameStateRepository:
    def find_by_path(self, path: str) -> GameState:
        with open(path, 'r') as file:
            board_data = json.load(file)

        board = Board()

        peg_track_positions = board_data["board"]
        for i, color in enumerate(Color):
            for j, track_position in enumerate(peg_track_positions[color.lower()]):
                peg = Peg((i * 4) + j, color)
                if track_position == -1:
                    board.add_peg(peg)
                else:
                    board.add_peg_at_track_position(peg, track_position)

        return GameState(
            color=Color.from_string(board_data["color"]),
            color_turns=board_data["color_turns"],
            board=board,
            roll=board_data["roll"]
        )