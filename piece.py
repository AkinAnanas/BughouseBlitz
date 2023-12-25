from constants import *
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
        self.piece_type = t
        self.has_moved = False  # for castling and pawn movement
        self.captured = False
        self.name = ['b', 'w'][self.color] + t
        self.rect = None
        self.value = MATERIAL_VALUES[t]  # the material value of the piece
        self.possible_moves = []
        self.calculated_moves = False

    def capture(self):
        self.captured = True
        self.pos = (-1, -1)

    def get_possible_moves(self):
        return []

    def copy(self, board, cls):
        piece = cls(board, self.pos[0], self.pos[1], self.color)
        piece.has_moved = self.has_moved
        piece.captured = self.captured
        piece.value = self.value
        piece.name = self.name
        return piece

    def __str__(self):
        return self.name


class Pawn(Piece):
    def __init__(self, b, x, y, c):
        super(Pawn, self).__init__(b, x, y, c, '')
        self.en_passant = False

    def get_possible_moves(self):
        if self.captured:
            return []
        direction = 1 if self.color == WHITE else -1
        possible_moves = []
        # only calculate possible moves once for performance purposes
        if self.calculated_moves:
            return self.possible_moves
        # moving vertically
        move1 = [self.pos[0], self.pos[1] + direction]
        move2 = [self.pos[0], self.pos[1] + direction * 2]
        #move2 = [self.pos[0], self.pos[1] + direction * 2, 'EN_PASSANT']
        if self.board.is_valid_move(self.pos, move1) and self.board.get_square(move1[0], move1[1]).is_empty():
            possible_moves.append(move1)
        if self.board.is_valid_move(self.pos, move2) and self.board.get_square(move2[0], move2[1]).is_empty() and not self.has_moved:
            possible_moves.append(move2)
        # capturing diagonally
        diagonal_moves = [[self.pos[0] - 1, self.pos[1] + direction], [self.pos[0] + 1, self.pos[1] + direction]]
        for move in diagonal_moves:
            if self.board.is_valid_move(self.pos, move) and not self.board.get_square(move[0], move[1]).is_empty():
                possible_moves.append(move)
        self.possible_moves = possible_moves
        return possible_moves


class Rook(Piece):
    def __init__(self, b, x, y, c):
        super(Rook, self).__init__(b, x, y, c, 'R')

    def get_possible_moves(self):
        possible_moves = []
        # only calculate possible moves once for performance purposes
        if self.calculated_moves:
            return self.possible_moves
        # loop through the directions that the rook can move in
        for direction in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            i = 1
            valid = True
            while valid:
                # add all legal moves in a direction until a piece is hit
                move = [self.pos[0] + direction[0] * i, self.pos[1] + direction[1] * i]
                if self.board.is_valid_move(self.pos, move):
                    possible_moves.append(move)
                # keep checking until the square doesn't exist
                if not Square.is_valid(move[0], move[1]):
                    valid = False
                # once a piece is in the way, that's the last piece that can be added (can't jump through pieces)
                elif not self.board.get_square(move[0], move[1]).is_empty():
                    valid = False
                i += 1
        self.possible_moves = possible_moves
        return possible_moves


class Knight(Piece):
    def __init__(self, b, x, y, c):
        super(Knight, self).__init__(b, x, y, c, 'N')

    def get_possible_moves(self):
        if self.captured:
            return []
        # only calculate possible moves once for performance purposes
        if self.calculated_moves:
            return self.possible_moves
        possible_moves = [[self.pos[0] - 2, self.pos[1] + 1], [self.pos[0] - 2, self.pos[1] - 1],
                          [self.pos[0] + 2, self.pos[1] + 1], [self.pos[0] + 2, self.pos[1] - 1],
                          [self.pos[0] + 1, self.pos[1] - 2], [self.pos[0] - 1, self.pos[1] - 2],
                          [self.pos[0] + 1, self.pos[1] + 2], [self.pos[0] - 1, self.pos[1] + 2]]
        for i in reversed(range(len(possible_moves))):
            move = possible_moves[i]
            if not self.board.is_valid_move(self.pos, move):
                del possible_moves[i]
        self.possible_moves = possible_moves
        return possible_moves


class Bishop(Piece):
    def __init__(self, b, x, y, c):
        super(Bishop, self).__init__(b, x, y, c, 'B')

    def get_possible_moves(self):
        possible_moves = []
        # only calculate possible moves once for performance purposes
        if self.calculated_moves:
            return self.possible_moves
        # loop through the directions that the rook can move in
        for direction in [[-1, -1], [-1, 1], [1, -1], [1, 1]]:
            i = 1
            valid = True
            while valid:
                # add all legal moves in a direction until a piece is hit
                move = [self.pos[0] + direction[0] * i, self.pos[1] + direction[1] * i]
                if self.board.is_valid_move(self.pos, move):
                    possible_moves.append(move)
                # not a valid move
                else:
                    valid = False
                # once a piece is in the way, that's the last piece that can be added (can't jump through pieces)
                square = self.board.get_square(move[0], move[1])
                piece = self.board.get_piece(move[0], move[1])
                if square is None or not square.is_empty():
                    valid = False
                i += 1
        self.possible_moves = possible_moves
        return possible_moves


class Queen(Piece):
    def __init__(self, b, x, y, c):
        super(Queen, self).__init__(b, x, y, c, 'Q')

    def get_possible_moves(self):
        possible_moves = []
        # only calculate possible moves once for performance purposes
        if self.calculated_moves:
            return self.possible_moves
        # loop through the directions that the rook can move in
        for direction in [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]:
            i = 1
            valid = True
            while valid:
                # add all legal moves in a direction until a piece is hit
                move = [self.pos[0] + direction[0] * i, self.pos[1] + direction[1] * i]
                if self.board.is_valid_move(self.pos, move):
                    possible_moves.append(move)
                # keep checking until the square doesn't exist
                if not Square.is_valid(move[0], move[1]):
                    valid = False
                # once a piece is in the way, that's the last piece that can be added (can't jump through pieces)
                elif not self.board.get_square(move[0], move[1]).is_empty():
                    valid = False
                i += 1
        self.possible_moves = possible_moves
        return possible_moves


class King(Piece):
    def __init__(self, b, x, y, c):
        super(King, self).__init__(b, x, y, c, 'K')
        self.castle_squares = {
            'K': [[self.pos[0] + 1, self.pos[1]], [self.pos[0] + 2, self.pos[1]]],
            'Q': [[self.pos[0] - 1, self.pos[1]], [self.pos[0] - 2, self.pos[1]], [self.pos[0] - 3, self.pos[1]]]
        }

    def get_possible_moves(self):
        possible_moves = []
        # only calculate possible moves once for performance purposes
        if self.calculated_moves:
            return self.possible_moves
        # loop through the directions that the rook can move in
        for direction in [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, 1], [1, -1], [1, 1]]:
            # add all legal moves in a direction until a piece is hit
            move = [self.pos[0] + direction[0], self.pos[1] + direction[1]]
            if self.board.is_valid_move(self.pos, move):
                possible_moves.append(move)
        # add castling moves
        if self.can_castle('K'):
            move = self.castle_squares['K'][-1].copy()
            possible_moves.append(move.append('CASTLING'))
        if self.can_castle('Q'):
            move = self.castle_squares['Q'][-1].copy()
            possible_moves.append(move.append('CASTLING'))
        self.possible_moves = possible_moves
        return possible_moves

    def can_castle(self, side='K'):
        squares = self.castle_squares[side]
        empty = True
        for sqr in squares:
            if not self.board.get_square(sqr[0], sqr[1]).is_empty():
                empty = False
        moved = self.has_moved
        rooks = self.board.get_pieces_by_type('R')
        for rook in rooks:
            if rook.color == self.color and (rook.captured or rook.has_moved):
                moved = True
        return empty and not moved

    def in_check(self):
        # get the opponent's color
        opponent = WHITE if self.color == BLACK else BLACK
        attackers = self.board.get_pieces_by_color(opponent)
        for piece in attackers:
            if list(self.pos) in piece.get_possible_moves():
                piece.get_possible_moves()
                return True
        return False
