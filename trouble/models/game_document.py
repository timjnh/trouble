from beanie import Document
from typing import List, Dict
from pydantic import BaseModel

from ..board import Board

class BoardModel(BaseModel):
    on_deck: List[str]
    color_by_board_position: Dict[int, str]
    final_slots: List[str]

    @classmethod
    def from_board(cls, board: Board) -> "BoardModel":
        color_by_board_position: Dict[int, str] = {}
        for peg in board.get_pegs_on_board():
            board_position = board.get_board_position_for_peg(peg)
            assert board_position is not None
            color_by_board_position[board_position] = str(peg.color)

        return cls(
            on_deck=[str(peg.color) for peg in board.pegs if board.is_peg_on_deck(peg)],
            color_by_board_position=color_by_board_position,
            final_slots=[str(peg.color) for peg in board.pegs if board.is_peg_in_final_slots(peg)],
        )

class TurnModel(BaseModel):
    color: str
    color_turns: int
    board: BoardModel
    roll: int

class GameDocument(Document):
    turns: List[TurnModel]
    winner: str