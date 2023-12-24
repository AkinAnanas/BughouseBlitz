from constants import *


class Square:
    def __init__(self, b, x, y):
        self.board = b
        self.file = FILES[x]
        self.rank = RANKS[y]
        self.pos = (x, y)
        self.name = f"{self.file}{self.rank}"
        self.color = BLACK if (x + y) % 2 == 0 else WHITE
        self.rect = None
        self.circle = None

    def is_empty(self):
        return self.board.get_piece(self.pos[0], self.pos[1]) is None

    @staticmethod
    def is_valid(x, y):
        return -1 < x < len(FILES) and -1 < y < len(RANKS)
