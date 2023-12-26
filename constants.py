
RANKS = list(range(1, 9))
FILES = "abcdefgh"
BLACK = 0
WHITE = 1
RANK_COUNT = 8
FILE_COUNT = 8
HUMAN = 0
AI = 1

GAME_TYPES = {
    'UNDEFINED': -1, 'P/P': 0, 'P/CPU': 1,
    'CPU/CPU': 2, 'P+CPU/CPU+CPU': 3,
    'P+P/CPU+CPU': 4, 'P+P/P+P': 5
}
MOVE_TYPES = {
    'ILLEGAL': -1, 'NORMAL': 0, 'PAWN_JUMP': 1,
    'CASTLING': 2, 'EN_PASSANT': 3
}
PRESET_TIME_CONTROLS = {
    'BULLET': [1, 1], 'BLITZ': [5, 3],
    'RAPID': [10, 0], 'CLASSICAL': [180, 0]
}
