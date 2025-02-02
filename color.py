from enum import StrEnum

class Color(StrEnum):
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'

    @classmethod
    def ordinal(cls, c: "Color") -> int:
        return list(Color).index(c)