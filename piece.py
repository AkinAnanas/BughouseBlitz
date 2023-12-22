from square import Square

MATERIAL_VALUES = {
    '': 1, 'R': 5,
    'N': 3, 'B': 3,
    'Q': 9, 'K': float('inf')
}


class Piece:
    def __init__(self, b, x, y, c, t):
        self.board = b
        self.pos = (x, y)
        self.color = c
        self.type = t
        self.has_moved = False  # for castling and pawn movement
        self.captured = False
        self.name = ['b', 'w'][self.color] + t
        self.rect = None
        self.value = MATERIAL_VALUES[t]  # the material value of the piece

    def capture(self):
        self.captured = True
        self.pos = [-1, -1]

    def get_possible_moves(self):
        return []

    def __str__(self):
        return self.name


class Pawn(Piece):
    def __init__(self, b, x, y, c):
        super(Pawn, self).__init__(b, x, y, c, '')


class Rook(Piece):
    def __init__(self, b, x, y, c):
        super(Rook, self).__init__(b, x, y, c, 'R')


class Knight(Piece):
    def __init__(self, b, x, y, c):
        super(Knight, self).__init__(b, x, y, c, 'N')

    def get_possible_moves(self):
        possible_moves = [[self.pos[0] - 2, self.pos[1] + 1], [self.pos[0] - 2, self.pos[1] - 1],
                          [self.pos[0] + 2, self.pos[1] + 1], [self.pos[0] + 2, self.pos[1] - 1],
                          [self.pos[0] + 1, self.pos[1] - 2], [self.pos[0] - 1, self.pos[1] - 2],
                          [self.pos[0] + 1, self.pos[1] + 2], [self.pos[0] - 1, self.pos[1] + 2]]
        for i in reversed(range(len(possible_moves))):
            move = possible_moves[i]
            if not Square.is_valid(move[0], move[1]):
                del possible_moves[i]
        return possible_moves


class Bishop(Piece):
    def __init__(self, b, x, y, c):
        super(Bishop, self).__init__(b, x, y, c, 'B')


class Queen(Piece):
    def __init__(self, b, x, y, c):
        super(Queen, self).__init__(b, x, y, c, 'Q')


class King(Piece):
    def __init__(self, b, x, y, c):
        super(King, self).__init__(b, x, y, c, 'K')
        self.in_check = False
