from uuid import uuid4

from .color import Color

type PegId = int

class Peg:
    def __init__(self, id: PegId, color: Color):
        self.id = id
        self.color = color