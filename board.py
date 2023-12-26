import utils
from constants import MOVE_TYPES
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
        self.en_passant_pawn = None

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

    def move(self, start_pos, dest_pos, capture=False):
        """
        move a piece to the specified location and play a sound
        :param start_pos: list representing the starting location
        :param dest_pos: list representing the ending location
        :param capture: bool representing whether the move captures a piece or not
        :return: None
        """
        piece1 = self.get_piece(start_pos[0], start_pos[1])
        piece2 = self.get_piece(dest_pos[0], dest_pos[1])
        piece1.pos = tuple(dest_pos)
        piece1.has_moved = True
        if piece2 is not None:
            piece2.capture()
        # if this is not a copy, play the move sound
        if self.index > -1:
            utils.play_sound('CAPTURE' if capture else 'MOVE')

    def is_valid_move(self, start_pos, dest_pos):
        """
        checks if a move is valid, meaning:
        the player can't move off of the board and,
        the player can't capture their own piece
        :param start_pos: list representing the starting location
        :param dest_pos: list representing the ending location
        :return: bool
        """
        piece1 = self.get_piece(start_pos[0], start_pos[1])
        piece2 = self.get_piece(dest_pos[0], dest_pos[1])
        # cannot capture your own piece
        if piece2 is not None and piece1.color == piece2.color:
            return False
        # cannot move out of bounds
        if not Square.is_valid(dest_pos[0], dest_pos[1]):
            return False
        return True

    def is_legal_move(self, start_pos, dest_pos, move_type=MOVE_TYPES['NORMAL']):
        """
        checks if a move is legal (meaning the move doesn't place one's own king in check)
        :param start_pos: list representing the starting location
        :param dest_pos: list representing the ending location
        :param move_type: int representing the move type
        :return: bool
        """
        piece1 = self.get_piece(start_pos[0], start_pos[1])
        if move_type == MOVE_TYPES['NORMAL'] or move_type == MOVE_TYPES['PAWN_JUMP']:
            # not legal if move allows own king to be in check
            next_board = self.copy()
            next_board.move(start_pos, dest_pos)
            return not next_board.get_king(piece1.color).in_check()
        if move_type == MOVE_TYPES['CASTLING']:
            # can't castle in check
            if self.get_king(piece1.color).in_check():
                return False
            # get the castle squares and castle type
            castle_type = 'Q' if dest_pos[0] == 2 else 'K'
            castle_squares = King.get_castle_squares(piece1.color, castle_type)
            # move king through the castle squares
            for square in castle_squares:
                next_board = self.copy()
                next_board.move(start_pos, square)
                # king can't castle through check
                if next_board.get_king(piece1.color).in_check():
                    return False
        return True

    def is_checkmate(self, color):
        """
        checks if the black or white king is in checkmate
        :param color: int representing black or white
        :return: bool
        """
        if not self.get_king(color).in_check():
            return False
        pieces = self.get_pieces_by_color(color)
        for piece in pieces:
            for move in piece.get_possible_moves():
                move_type = MOVE_TYPES['NORMAL'] if len(move) == 2 else MOVE_TYPES[move[-1]]
                if self.is_legal_move(piece.pos, move[0:2], move_type):
                    return False
        return True

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
        # create a new board
        board = Board()
        board.pieces.clear()
        # copy the pieces
        for piece in self.pieces:
            board.pieces.append(piece.copy(board, type(piece)))
        # copy the en passant pawn if it exists
        if self.en_passant_pawn is not None:
            pawn_pos = self.en_passant_pawn.pos
            pawn = board.get_piece(pawn_pos[0], pawn_pos[1])
            board.en_passant_pawn = pawn
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
