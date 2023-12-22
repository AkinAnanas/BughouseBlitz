import utils


class Theme:
    def __init__(self):
        self.light = utils.from_hex("eeeed2")
        self.dark = utils.from_hex("769656")
        self.background = utils.from_hex("baca44")
        self.highlight = utils.from_hex("FFA500")
        self.accent = utils.from_hex("#ffffff")

    @staticmethod
    def create(light, dark, background, highlight, accent):
        theme = Theme()
        theme.light = light
        theme.dark = dark
        theme.background = background
        theme.highlight = highlight
        theme.accent = accent
        return theme


# TODO: create other themes (light, dark, etc)
THEMES = {
    'DEFAULT': Theme(),
    'LIGHT': Theme.create(
        utils.from_rgba(232, 235, 239, 255),
        utils.from_rgba(125, 135, 150, 255),
        utils.from_preset('BLUE'),
        utils.from_preset('BLUE'),
        utils.from_preset('BLUE'),
    )
}
