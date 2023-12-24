import utils


class Theme:
    def __init__(self):
        self.light = utils.from_hex('eeeed2')
        self.dark = utils.from_hex('769656')
        self.background = utils.from_hex('baca44')
        self.highlight = utils.from_hex('145A32')
        self.accent = utils.from_hex('eeeed2')
        self.danger = utils.from_preset('RED')
        self.contrast = utils.from_hex('145A32')

    @staticmethod
    def create(light, dark, background, highlight, accent,
               danger=utils.from_preset('RED'),
               contrast=utils.from_preset('GRAY')):
        theme = Theme()
        theme.light = light
        theme.dark = dark
        theme.background = background
        theme.highlight = highlight
        theme.accent = accent
        theme.danger = danger
        theme.contrast = contrast
        return theme


# TODO: create other themes (light, dark, etc)
THEMES = {
    'DEFAULT': Theme(),
    'BLUE': Theme.create(
        utils.from_rgba(232, 235, 239, 255),
        utils.from_rgba(125, 135, 150, 255),
        utils.from_hex('B0C4DE'),
        utils.from_hex('34495E'),
        utils.from_preset('WHITE'),
        contrast=utils.from_hex('34495E'),
    )
}
