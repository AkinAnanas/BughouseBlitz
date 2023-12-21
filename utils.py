import math


def from_rgba(r, g, b, a):
    return r / 255.0, g / 255.0, b / 255.0, a / 255.0


def from_hex(hex_str):
    c = hex_str[1:] if hex_str[0] == '#' else hex_str
    r = int(c[0:2], 16)
    g = int(c[2:4], 16)
    b = int(c[4:6], 16)
    a = 255 if len(c) < 7 else int(c[6:8], 16)
    return from_rgba(r, g, b, a)


def multiply_colors(c1, c2):
    return [f1 * f2 for f1, f2 in zip(c1, c2)]


def dist(x1, y1, x2, y2):
    return math.sqrt(pow((x2 - x1), 2) + pow((y2 - y1), 2))
