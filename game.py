import utils
from board import *
from random import randrange


HUMAN = 0
AI = 1
GAME_TYPES = {
    'UNDEFINED': -1, 'P/P': 0, 'P/CPU': 1,
    'CPU/CPU': 2, 'P+CPU/CPU+CPU': 3,
    'P+P/CPU+CPU': 4, 'P+P/P+P': 5
}

PRESET_TIME_CONTROLS = {
    'BULLET': [1, 1], 'BLITZ': [5, 3],
    'RAPID': [10, 0], 'CLASSICAL': [180, 0]
}


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

    def end_game(self):
        pass

    def move(self, start_pos, dest_pos):
        next_board = self.board.copy()
        next_board.index += 1
        piece1 = next_board.get_piece(start_pos[0], start_pos[1])
        piece2 = next_board.get_piece(dest_pos[0], dest_pos[1])
        if piece1 is None or not self.validate_move(start_pos, dest_pos):
            return False  # move unsuccessful
        piece1.pos = dest_pos
        # handle capturing of the piece
        if piece2 is not None:
            piece2.capture()
            utils.play_sound('CAPTURE')
        else:
            utils.play_sound('MOVE')
        # update the board and view_board
        self.board = next_board
        self.view_board = self.board
        self.index = self.view_board.index
        self.boards.append(self.board)
        # update turns
        self.turn = WHITE if self.turn == BLACK else BLACK  # toggle who moves
        if piece1.color == WHITE:
            self.moves += 1
        return True  # move successful

    def validate_move(self, start_pos, dest_pos):
        piece1 = self.board.get_piece(start_pos[0], start_pos[1])
        piece2 = self.board.get_piece(dest_pos[0], dest_pos[1])
        #  if the game type is undefined, there can't be a piece
        #  in the destination position for the move to be considered 'legal'
        if self.game_type == GAME_TYPES['UNDEFINED'] and piece2 is not None:
            return False
        #  if it is a regular game, there can't be a piece of the same color
        #  in the destination position for the move to be considered 'legal'
        if self.game_type != GAME_TYPES['UNDEFINED']:
            return self.board.is_legal_move(start_pos, dest_pos)
        return True

    def next(self):
        if self.index < len(self.boards) - 1:
            self.index += 1
            self.view_board = self.boards[self.index]

    def back(self):
        if self.index > 0:
            self.index -= 1
            self.view_board = self.boards[self.index]
