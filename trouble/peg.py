from uuid import uuid4

from .color import Color

class Peg:
    def __init__(self, color: Color):
        self.id = uuid4()
        self.color = color