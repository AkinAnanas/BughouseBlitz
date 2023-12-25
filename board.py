from constants import *
from piece import *
from square import Square


class Board:
    def __init__(self):
        self.index = -1
        self.squares = []
        # initialize the squares
        for y in range(FILE_COUNT):
            for x in range(RANK_COUNT):
                self.squares.append(Square(self, x, y))

        self.pieces = []
        self.setup_board()

    def get_piece(self, x, y) -> Piece | None:
        for piece in self.pieces:
            if piece.pos == (x, y):
                return piece
        return None

    def get_pieces_by_color(self, color) -> [Piece]:
        pieces = []
        for piece in self.pieces:
            if piece.color == color:
                pieces.append(piece)
        return pieces

    def get_pieces_by_type(self, piece_type):
        pieces = []
        for piece in self.pieces:
            if piece.piece_type == piece_type:
                pieces.append(piece)
        return pieces

    def get_square(self, x, y) -> Square | None:
        for sqr in self.squares:
            if sqr.pos == (x, y):
                return sqr
        return None

    def get_king(self, color) -> King:
        for piece in self.pieces:
            if piece.piece_type == 'K' and piece.color == color:
                return piece

    def get_en_passant_pawn(self) -> Pawn | None:
        for piece in self.pieces:
            if piece.piece_type == '':
                if piece.en_passant:
                    return piece
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

    def move(self, start_pos, dest_pos):
        piece1 = self.get_piece(start_pos[0], start_pos[1])
        piece2 = self.get_piece(dest_pos[0], dest_pos[1])
        piece1.pos = tuple(dest_pos)
        piece1.has_moved = True
        if piece2 is not None:
            piece2.capture()

    def is_valid_move(self, start_pos, dest_pos):
        piece1 = self.get_piece(start_pos[0], start_pos[1])
        piece2 = self.get_piece(dest_pos[0], dest_pos[1])
        # cannot capture your own piece
        if piece2 is not None and piece1.color == piece2.color:
            return False
        # cannot move out of bounds
        if not Square.is_valid(dest_pos[0], dest_pos[1]):
            return False
        return True

    def is_legal_move(self, start_pos, dest_pos):
        piece1 = self.get_piece(start_pos[0], start_pos[1])
        # not legal if move allows own king to be in check
        next_board = self.copy()
        next_board.move(start_pos, dest_pos)
        return not next_board.get_king(piece1.color).in_check()

    @staticmethod
    def from_str(data):
        board = Board()
        board.pieces.clear()
        lines = data.split('\n')
        for y in range(len(lines)):
            cols = lines[y].split('.')
            for x in range(len(cols)):
                code = cols[x]
                color = WHITE if code[0] == 'w' else BLACK
                if len(code) == 1:
                    match code[0]:
                        case '-':
                            continue
                        case 'w':
                            p = Pawn(board, x, y, color)
                            board.pieces.append(p)
                        case 'b':
                            p = Pawn(board, x, y, color)
                            board.pieces.append(p)
                else:
                    match code[1]:
                        case 'Q':
                            q = Queen(board, x, y, color)
                            board.pieces.append(q)
                        case 'K':
                            k = King(board, x, y, color)
                            board.pieces.append(k)
                        case 'N':
                            n = Knight(board, x, y, color)
                            board.pieces.append(n)
                        case 'B':
                            b = Bishop(board, x, y, color)
                            board.pieces.append(b)
                        case 'R':
                            r = Rook(board, x, y, color)
                            board.pieces.append(r)
        return board

    def copy(self):
        board = Board()
        board.pieces.clear()
        for piece in self.pieces:
            board.pieces.append(piece.copy(board, type(piece)))
        return board

    def __str__(self):
        board_str = ""
        for y in range(FILE_COUNT):
            for x in range(RANK_COUNT):
                p = self.get_piece(x, y)
                board_str += ('-' if p is None else p.name)
                if x < RANK_COUNT - 1:
                    board_str += '.'
            if y < FILE_COUNT - 1:
                board_str += '\n'
        return board_str
