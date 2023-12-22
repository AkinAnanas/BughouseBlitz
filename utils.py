import math
from kivy.core.audio import Sound, SoundLoader

PRESET_COLORS = {
    'WHITE': [1, 1, 1, 1],
    'BLACK': [0, 0, 0, 0],
    'RED': [1, 0, 0, 1],
    'BLUE': [0, 0, 1, 1],
    'GREEN': [0, 1, 0, 1],
    'GRAY': [.5, .5, .5, 1]
}

GAME_SOUNDS: dict[str, Sound] = {
    'MOVE': SoundLoader.load('assets/sounds/move.wav'),
    'CAPTURE': SoundLoader.load('assets/sounds/capture.wav'),
    'NOTIFY': SoundLoader.load('assets/sounds/notify.wav')
}


def from_rgba(r, g, b, a):
    return r / 255.0, g / 255.0, b / 255.0, a / 255.0


def from_hex(hex_str):
    c = hex_str[1:] if hex_str[0] == '#' else hex_str
    r = int(c[0:2], 16)
    g = int(c[2:4], 16)
    b = int(c[4:6], 16)
    a = 255 if len(c) < 7 else int(c[6:8], 16)
    return from_rgba(r, g, b, a)


def from_preset(name):
    return PRESET_COLORS[name]


def play_sound(name):
    GAME_SOUNDS[name].play()


def multiply_colors(c1, c2):
    return [f1 * f2 for f1, f2 in zip(c1, c2)]


def dist(x1, y1, x2, y2):
    return math.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))
