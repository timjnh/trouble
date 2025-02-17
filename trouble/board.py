from typing import List, Dict

from .peg import Peg
from .color import Color

class Board:
    FULL_TRACK_LENGTH = 32 # includes the final four slots
    INTERIOR_TRACK_LENGTH = FULL_TRACK_LENGTH - 4

    def __init__(self):
        self.pegs_by_color: Dict[Color, List[Peg]] = {}

    def reset(self):
        for c in Color:
            if self.pegs_by_color.get(c) is not None:
                for p in self.pegs_by_color[c]:
                    p.reset()

    def add_pegs(self, pegs: List[Peg]):
        for p in pegs:
            assert p.position is None or p.position < self.FULL_TRACK_LENGTH

            board_position = self.get_board_peg_position(p)
            if board_position is not None:
                assert not self.get_peg_at_board_position(board_position)

            if p.color not in self.pegs_by_color:
                self.pegs_by_color[p.color] = []
            self.pegs_by_color[p.color].append(p)

    @property
    def pegs(self) -> List[Peg]:
        return [peg for peg_list in self.pegs_by_color.values() for peg in peg_list]

    def get_pegs_on_board(self, color: Color) -> List[Peg]:
        return [p for p in self.pegs_by_color[color] if p.is_on_board and p.position is not None and p.position < self.INTERIOR_TRACK_LENGTH]

    def get_pegs_on_deck(self, color: Color) -> List[Peg]:
        return [p for p in self.pegs_by_color[color] if p.is_on_deck]
    
    def get_pegs_in_final_slots(self, color: Color) -> List[Peg]:
        if self.pegs_by_color.get(color) is None:
            return []
        return [p for p in self.pegs_by_color[color] if p.position is not None and p.position >= self.FULL_TRACK_LENGTH - 4]
    
    def get_board_peg_position(self, peg: Peg) -> int | None:
        if peg.position is None:
            return None

        if peg.position >= self.FULL_TRACK_LENGTH - 4:
            return None
        
        return self.track_position_to_board_position(peg.position, peg.color)
    
    def track_position_to_board_position(self, track_position: int, color: Color) -> int:
        color_offset = int(self.INTERIOR_TRACK_LENGTH / 4)
        return (track_position + Color.ordinal(color) * color_offset) % Board.INTERIOR_TRACK_LENGTH
    
    def board_position_to_track_position(self, board_position: int, color: Color) -> int:
        color_offset = int(self.INTERIOR_TRACK_LENGTH / 4)
        board_start_position = Color.ordinal(color) * color_offset
        if board_position >= board_start_position:
            return board_position - board_start_position
        else:
            return board_position + (Board.INTERIOR_TRACK_LENGTH - board_start_position)
        
    def get_peg_at_board_position(self, board_position: int) -> Peg | None:
        for peg in self.pegs:
            if self.get_board_peg_position(peg) == board_position:
                return peg
        return None