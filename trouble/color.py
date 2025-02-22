from enum import StrEnum

class Color(StrEnum):
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    BLUE = 'blue'

    def __str__(self) -> str:
        if(self == Color.RED):
            return '\033[91mR'
        elif(self == Color.YELLOW):
            return '\033[93mY'
        elif(self == Color.GREEN):
            return '\033[92mG'
        else:
            return '\033[94mB' # BLUE

    @classmethod
    def ordinal(cls, c: "Color") -> int:
        return list(Color).index(c)
    
    @classmethod
    def next(cls, c: "Color") -> "Color":
        return list(Color)[(cls.ordinal(c) + 1) % len(Color)]