from piece import *

BLACK = 0
WHITE = 1
RANKS = list(range(1, 9))
FILES = "abcdefgh"
RANK_COUNT = 8
FILE_COUNT = 8


class Square:
    def __init__(self, b, x, y):
        self.board = b
        self.file = FILES[x]
        self.rank = RANKS[y]
        self.pos = (x, y)
        self.name = f"{self.file}{self.rank}"
        self.color = BLACK if (x + y) % 2 == 0 else WHITE
        self.rect = None


class Board:
    def __init__(self):
        self.squares = []
        # initialize the squares
        for y in range(FILE_COUNT):
            for x in range(RANK_COUNT):
                self.squares.append(Square(self, x, y))

        self.pieces = []
        self.setup_board()

    def get_piece(self, x, y):
        for piece in self.pieces:
            if piece.pos == (x, y):
                return piece
        return None

    def get_square(self, x, y):
        for sqr in self.squares:
            if sqr.pos == (x, y):
                return sqr
        return None

    # initialize all the pieces and squares
    def setup_board(self):
        self.pieces.clear()
        # initialize the pieces
        for i in range(FILE_COUNT):
            # create the pawns
            wp = Pawn(self, i, 1, WHITE)
            bp = Pawn(self, i, 6, BLACK)
            # add the pawns
            self.pieces.append(wp)
            self.pieces.append(bp)
        # create the rooks
        wr1 = Rook(self, 0, 0, WHITE)
        wr2 = Rook(self, 7, 0, WHITE)
        br1 = Rook(self, 0, 7, BLACK)
        br2 = Rook(self, 7, 7, BLACK)
        # create the knights
        wn1 = Knight(self, 1, 0, WHITE)
        wn2 = Knight(self, 6, 0, WHITE)
        bn1 = Knight(self, 1, 7, BLACK)
        bn2 = Knight(self, 6, 7, BLACK)
        # create the bishops
        wb1 = Bishop(self, 2, 0, WHITE)
        wb2 = Bishop(self, 5, 0, WHITE)
        bb1 = Bishop(self, 2, 7, BLACK)
        bb2 = Bishop(self, 5, 7, BLACK)
        # create the queens
        wq = Queen(self, 3, 0, WHITE)
        bq = Queen(self, 3, 7, BLACK)
        # create the kings
        wk = King(self, 4, 0, WHITE)
        bk = King(self, 4, 7, BLACK)
        # add the rest of the pieces
        for p in [wr1, wr2, br1, br2, wn1, wn2, bn1,
                  bn2, wb1, wb2, bb1, bb2, wq, bq, wk, bk]:
            self.pieces.append(p)

    @staticmethod
    def from_str(data):
        board = Board()
        board.pieces.clear()
        lines = data.split('\n')
        for y in range(len(lines)):
            cols = lines[y].split('.')
            for x in range(len(cols)):
                match cols[x]:
                    # pawns
                    case 'w':
                        wp = Pawn(board, x, y, WHITE)
                        board.pieces.append(wp)
                    case 'b':
                        bp = Pawn(board, x, y, BLACK)
                        board.pieces.append(bp)
                    #
        return board

    def __copy__(self):
        pass

    def __str__(self):
        board_str = ""
        for y in range(FILE_COUNT):
            for x in range(RANK_COUNT):
                p = self.get_piece(x, y)
                board_str += ('-' if p is None else p.name)
                board_str += '.'
            board_str += '\n'
        return board_str
