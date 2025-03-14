from typing import Self
from enum import StrEnum

class Color(StrEnum):
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'

    def __str__(self) -> str:
        if(self == Color.RED):
            return 'R'
        elif(self == Color.YELLOW):
            return 'Y'
        elif(self == Color.GREEN):
            return 'G'
        else:
            return 'B' # BLUE
        
    @classmethod
    def from_string(cls, color: str) -> "Color":
        if color == 'R':
            return Color.RED
        elif color == 'G':
            return Color.GREEN
        elif color == 'Y':
            return Color.YELLOW
        else:
            return Color.BLUE
        
    def to_styled_string(self) -> str:
        return Color.color_code(self) + str(self)

    @classmethod
    def ordinal(cls, c: "Color") -> int:
        return list(Color).index(c)
    
    @classmethod
    def from_ordinal(cls, ordinal: int) -> "Color":
        return list(Color)[ordinal % len(Color)]
    
    @classmethod
    def next(cls, c: "Color") -> "Color":
        return list(Color)[(cls.ordinal(c) + 1) % len(Color)]
    
    @classmethod
    def color_code(cls, color: Self) -> str:
        if color == Color.RED:
            return '\033[91m'
        elif color == Color.YELLOW:
            return '\033[93m'
        elif color == Color.GREEN:
            return '\033[92m'
        else:
            return '\033[94m'