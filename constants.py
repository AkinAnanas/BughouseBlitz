
RANKS = list(range(1, 9))
FILES = "abcdefgh"
BLACK = 0
WHITE = 1
RANK_COUNT = 8
FILE_COUNT = 8

GAME_TYPES = {
    'UNDEFINED': -1, 'P/P (Local)': 0, 'P/P (Online)': 1,
    'P+P/P+P (Online)': 2, 'P+P/P+P (Party)': 3
}
MOVE_TYPES = {
    'ILLEGAL': -1, 'NORMAL': 0, 'PAWN_JUMP': 1,
    'CASTLING': 2, 'EN_PASSANT': 3
}
PRESET_TIME_CONTROLS = {
    'BULLET': [1, 1], 'BLITZ': [5, 3],
    'RAPID': [10, 0], 'CLASSICAL': [180, 0],
    'UNLIMITED': [float('inf'), 0]
}
