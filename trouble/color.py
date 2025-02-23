from typing import Self
from enum import StrEnum

class Color(StrEnum):
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'

    def __str__(self) -> str:
        char = ''
        if(self == Color.RED):
            char = 'R'
        elif(self == Color.YELLOW):
            char = 'Y'
        elif(self == Color.GREEN):
            char = 'G'
        else:
            char = 'B' # BLUE
        return Color.color_code(self) + char

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