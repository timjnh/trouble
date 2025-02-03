from enum import StrEnum

class Color(StrEnum):
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'

    @classmethod
    def ordinal(cls, c: "Color") -> int:
        return list(Color).index(c)
    
    @classmethod
    def next(cls, c: "Color") -> "Color":
        return list(Color)[(cls.ordinal(c) + 1) % len(Color)]