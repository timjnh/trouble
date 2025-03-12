from beanie import Document
from typing import List, Dict
from pydantic import BaseModel

from .. import Board, Color

class BoardModel(BaseModel):
    red: List[int]
    green: List[int]
    yellow: List[int]
    blue: List[int]

    @classmethod
    def from_board(cls, board: Board) -> "BoardModel":
        peg_positions_by_color: Dict[str, List[int]] = {}

        for color in Color:
            peg_positions_by_color[color] = []

            pegs = board.get_pegs_by_color(color)
            sorted_pegs = sorted(pegs, key=lambda peg: peg.id)

            for peg in sorted_pegs:
                if board.is_peg_on_deck(peg):
                    peg_positions_by_color[color].append(-1)
                else:
                    track_position = board.get_track_position_for_peg(peg)
                    assert track_position is not None
                    peg_positions_by_color[color].append(track_position)

        return cls(**peg_positions_by_color)

class TurnModel(BaseModel):
    color: str
    color_turns: int
    board: BoardModel
    roll: int

class GameDocument(Document):
    turns: List[TurnModel]
    winner: str