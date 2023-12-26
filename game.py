import time

import utils
from board import *
from random import randrange

from constants import *


class Game:
    def __init__(self):
        self.board = Board()  # the current board state of the game
        self.board.index = 0
        self.view_board = self.board  # the board that is being viewed
        self.boards = [self.board]  # all the boards in the game so far
        self.turn = WHITE  # white starts first
        self.moves = 0  # move count
        self.notation = []  # the chess notation of the game
        self.white_player_type, self.black_player_type = HUMAN, HUMAN
        self.game_type = GAME_TYPES['UNDEFINED']  # before the game starts anything can be moved anywhere
        self.time_control = PRESET_TIME_CONTROLS['BLITZ']  # seconds + increments
        self.index = self.view_board.index
        self.multiplayer = False
        self.started = False

    def start_game(self, game_type):
        self.game_type = game_type
        self.board = Board()
        self.board.index = 0
        self.view_board = self.board
        self.index = self.view_board.index
        self.boards = [self.board]
        self.turn = WHITE
        self.moves = 0
        self.started = True

        # randomize who starts as white
        starts_white = randrange(0, 2) == 0
        # process the game type
        if game_type == GAME_TYPES['P/P']:
            self.white_player_type, self.black_player_type = HUMAN, HUMAN
        if game_type == GAME_TYPES['P/CPU']:
            self.white_player_type = HUMAN if starts_white else AI
            self.black_player_type = AI if starts_white else HUMAN
        utils.play_sound('NOTIFY')

    def end_game(self, winner):
        print('Winner:', winner)
        self.started = False
        self.game_type = GAME_TYPES['UNDEFINED']

    def move(self, start_pos, dest_pos):
        next_board = self.board.copy()
        next_board.index = self.index + 1
        piece1 = next_board.get_piece(start_pos[0], start_pos[1])
        piece2 = next_board.get_piece(dest_pos[0], dest_pos[1])
        move_type = self.validate_move(start_pos, dest_pos)
        if piece1 is None or move_type == MOVE_TYPES['ILLEGAL']:
            return False  # move is not valid
        if move_type == MOVE_TYPES['NORMAL']:
            next_board.move(start_pos, dest_pos, piece2 is not None)
            next_board.en_passant_pawn = None
        if move_type == MOVE_TYPES['PAWN_JUMP']:
            next_board.move(start_pos, dest_pos)
            next_board.en_passant_pawn = piece1
        if move_type == MOVE_TYPES['CASTLING']:
            # get the castle squares and castle type
            castle_type = 'Q' if dest_pos[0] == 2 else 'K'
            castle_squares = King.get_castle_squares(piece1.color, castle_type)
            # move the king to the last castle square
            next_board.move(start_pos, castle_squares[-1])
            time.sleep(.1)
            # move the rook to the first castle square
            rook_pos = [0 if castle_type == 'Q' else 7, 0 if piece1.color == WHITE else 7]
            next_board.move(rook_pos, castle_squares[0])
            next_board.en_passant_pawn = None
        if move_type == MOVE_TYPES['EN_PASSANT']:
            next_board.move(start_pos, dest_pos, True)
            next_board.en_passant_pawn.capture()
        # update the board and view_board
        self.board = next_board
        self.view_board = self.board
        self.index = self.view_board.index
        self.boards.append(self.board)
        # update turns
        prev = self.turn
        self.turn = WHITE if self.turn == BLACK else BLACK  # toggle who moves
        if piece1.color == WHITE:
            self.moves += 1
        if self.board.is_checkmate(self.turn):
            self.end_game(prev)
        return True  # move successful

    def validate_move(self, start_pos, dest_pos):
        move_type = MOVE_TYPES['NORMAL']
        # piece1 = piece being moved, piece2 = piece being captured if any
        piece1 = self.board.get_piece(start_pos[0], start_pos[1])
        piece2 = self.board.get_piece(dest_pos[0], dest_pos[1])
        #  if the game type is undefined, don't allow captures
        if piece1 is None or (self.game_type == GAME_TYPES['UNDEFINED'] and piece2 is not None):
            return MOVE_TYPES['ILLEGAL']
        if self.game_type != GAME_TYPES['UNDEFINED']:
            for move in piece1.get_possible_moves():
                if len(move) > 2:
                    move_type = MOVE_TYPES[move[-1]]
                # move is normal, handle it as such
                if list(dest_pos) == move[0:2] and self.board.is_legal_move(start_pos, dest_pos, move_type):
                    return move_type
            return MOVE_TYPES['ILLEGAL']
        return move_type

    def next(self):
        if self.index < len(self.boards) - 1:
            self.index += 1
            self.view_board = self.boards[self.index]

    def back(self):
        if self.index > 0:
            self.index -= 1
            self.view_board = self.boards[self.index]
