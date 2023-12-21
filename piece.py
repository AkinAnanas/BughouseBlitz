class Piece:
    def __init__(self, b, x, y, c, t):
        self.board = b
        self.pos = (x, y)
        self.color = c
        self.type = t
        self.hasMoved = False  # important for castling
        self.name = ['b', 'w'][self.color] + t
        self.rect = None

    def get_possible_moves(self):
        pass

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


class Bishop(Piece):
    def __init__(self, b, x, y, c):
        super(Bishop, self).__init__(b, x, y, c, 'B')


class Queen(Piece):
    def __init__(self, b, x, y, c):
        super(Queen, self).__init__(b, x, y, c, 'Q')


class King(Piece):
    def __init__(self, b, x, y, c):
        super(King, self).__init__(b, x, y, c, 'K')
