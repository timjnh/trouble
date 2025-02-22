from typing import List, Dict

from uuid import UUID

from .peg import Peg
from .color import Color

class Board:
    FULL_TRACK_LENGTH = 32 # includes the final four slots
    INTERIOR_TRACK_LENGTH = FULL_TRACK_LENGTH - 4

    def __init__(self):
        self.pegs_by_color: Dict[Color, List[Peg]] = {}
        self.pegs_by_color_and_track_position: Dict[Color, Dict[int, Peg]] = { color: {} for color in Color }
        self.track_position_by_peg: Dict[UUID, int] = {}
        self.pegs_by_board_position: Dict[int, Peg] = {}
        self.board_position_by_peg: Dict[UUID, int] = {}

    def __str__(self) -> str:
        result = "\033[97mOn Deck: "
        for color in Color:
            for peg in self.get_pegs_on_deck(color):
                result += f"{peg.color}"
        result += "\n"
        for i in range(self.INTERIOR_TRACK_LENGTH):
            peg = self.get_peg_at_board_position(i)
            if peg is not None:
                result += f"{peg.color}"
            else:
                result += "\033[97mO"
        return result

    def reset(self):
        self.pegs_by_board_position = {}
        self.board_position_by_peg = {}
        self.pegs_by_color_and_track_position = { color: {} for color in Color }
        self.track_position_by_peg = {}

    def add_peg(self, peg: Peg):
        assert peg.id not in [p.id for p in self.pegs]

        if peg.color not in self.pegs_by_color:
            self.pegs_by_color[peg.color] = []
        self.pegs_by_color[peg.color].append(peg)

    def add_peg_at_track_position(self, peg: Peg, track_position: int):
        self.add_peg(peg)
        self.set_peg_track_position(peg, track_position)

    def set_peg_track_position(self, peg: Peg, track_position: int):
        assert track_position >= 0 and track_position < self.FULL_TRACK_LENGTH
        assert self.pegs_by_color_and_track_position[peg.color].get(track_position) is None

        board_position = self.track_position_to_board_position(track_position, peg.color)
        assert board_position not in self.pegs_by_board_position

        # remove peg from old position
        old_board_position = self.board_position_by_peg.get(peg.id)
        if old_board_position is not None:
            old_track_position = self.board_position_to_track_position(old_board_position, peg.color)
            del self.pegs_by_board_position[old_board_position]
            del self.pegs_by_color_and_track_position[peg.color][old_track_position]
            del self.track_position_by_peg[peg.id]

        if board_position is not None:
            self.pegs_by_board_position[board_position] = peg
            self.board_position_by_peg[peg.id] = board_position
        self.pegs_by_color_and_track_position[peg.color][track_position] = peg
        self.track_position_by_peg[peg.id] = track_position

    def set_peg_on_deck(self, peg: Peg):
        board_position = self.board_position_by_peg.get(peg.id)
        if board_position is not None:
            del self.board_position_by_peg[peg.id]
            del self.pegs_by_board_position[board_position]
        track_position = self.track_position_by_peg.get(peg.id)
        if track_position is not None:
            del self.pegs_by_color_and_track_position[peg.color][track_position]
            del self.track_position_by_peg[peg.id]

    @property
    def pegs(self) -> List[Peg]:
        return [peg for peg_list in self.pegs_by_color.values() for peg in peg_list]
    
    def get_pegs_by_color(self, color: Color) -> List[Peg]:
        return self.pegs_by_color.get(color, [])

    def get_pegs_on_board(self, color: Color) -> List[Peg]:
        pegs_by_track_position = self.pegs_by_color_and_track_position[color]
        return [peg for position, peg in pegs_by_track_position.items() if position < self.INTERIOR_TRACK_LENGTH]

    def get_pegs_on_deck(self, color: Color) -> List[Peg]:
        return [peg for peg in self.pegs_by_color[color] if self.is_peg_on_deck(peg) == True]
    
    def is_peg_on_deck(self, peg: Peg) -> bool:
        track_position = self.track_position_by_peg.get(peg.id)
        return track_position is None

    def get_pegs_in_final_slots(self, color: Color) -> List[Peg]:
        pegs_by_track_position = self.pegs_by_color_and_track_position[color].values()
        return [peg for peg in pegs_by_track_position if self.is_peg_in_final_slots(peg) == True]
    
    def is_peg_in_final_slots(self, peg: Peg) -> bool:
        track_position = self.track_position_by_peg.get(peg.id)
        if track_position is None:
            return False
        return track_position >= self.INTERIOR_TRACK_LENGTH
    
    def get_peg_at_board_position(self, board_position: int) -> Peg | None:
        return self.pegs_by_board_position.get(board_position)
    
    def get_peg_at_track_position(self, track_position: int, color: Color) -> Peg | None:
        return self.pegs_by_color_and_track_position[color].get(track_position)
    
    def get_track_position_for_peg(self, peg: Peg) -> int | None:
        return self.track_position_by_peg.get(peg.id)

    def get_board_position_for_peg(self, peg: Peg) -> int | None:
        track_position = self.track_position_by_peg.get(peg.id)
        if track_position is None or track_position >= self.INTERIOR_TRACK_LENGTH:
            return None
        return self.track_position_to_board_position(track_position, peg.color)
    
    def track_position_to_board_position(self, track_position: int, color: Color) -> int | None:
        if track_position >= self.INTERIOR_TRACK_LENGTH:
            return None
        color_offset = int(self.INTERIOR_TRACK_LENGTH / 4)
        return (track_position + Color.ordinal(color) * color_offset) % Board.INTERIOR_TRACK_LENGTH
    
    def board_position_to_track_position(self, board_position: int, color: Color) -> int:
        color_offset = int(self.INTERIOR_TRACK_LENGTH / 4)
        board_start_position = Color.ordinal(color) * color_offset
        if board_position >= board_start_position:
            return board_position - board_start_position
        else:
            return board_position + (Board.INTERIOR_TRACK_LENGTH - board_start_position)
