import utils


class Theme:
    def __init__(self):
        self.light = utils.from_hex("eeeed2")
        self.dark = utils.from_hex("769656")
        self.background = utils.from_hex("baca44")
        self.highlight = utils.from_hex("FFA500")
        self.accent = utils.from_hex("#ffffff")

    def set(self, light, dark, background, highlight, accent):
        self.light = light
        self.dark = dark
        self.background = background
        self.highlight = highlight
        self.accent = accent


DEFAULT = Theme()

# TODO: create other themes (light, dark, etc)
