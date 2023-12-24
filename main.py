from kivy.app import App
from kivy.core.image import Image
from kivy.graphics import Color
from kivy.graphics import Rectangle, Ellipse
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button

from constants import *
from game import Game, GAME_TYPES
from theme import THEMES
import utils


class BoardWidget(Widget):
    def __init__(self, **kwargs):
        super(BoardWidget, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.game = Game()
        self.selected_square = None
        self.selected_piece = None
        self.theme = self.app.theme
        self.background = None
        self.popup = None
        self.draw_flipped = False
        self.auto_flip = True
        self.show_possible_moves = True
        self.margin = 0
        self.square_length = 0
        self.bind(size=self.render, pos=self.render)

    def render(self, *args):
        self.theme = self.app.theme
        self.canvas.clear()
        with self.canvas:
            # resize everything
            self.margin = self.width * .05
            self.square_length = (self.width - self.margin * 2) / RANK_COUNT
            self.render_squares()
            self.render_pieces()

    def render_pieces(self):
        self.render_possible_moves()
        # setup and draw all the pieces
        for piece in self.game.view_board.pieces:
            draw_pos = [RANK_COUNT - (piece.pos[0] + 1),
                        FILE_COUNT - (piece.pos[1] + 1)] if self.draw_flipped else piece.pos
            piece_pos = self.board_to_screen_pos(draw_pos)
            Color(1, 1, 1, 1, mode='rgba')
            texture = Image(f'assets/pieces/{piece.name}.png').texture
            piece.rect = Rectangle(texture=texture, pos=piece_pos, size=(self.square_length, self.square_length))

    def render_squares(self):
        # get the theme colors
        light, dark, bg = self.theme.light, self.theme.dark, self.theme.background
        # draw the background
        Color(bg[0], bg[1], bg[2], bg[3], mode='rgba')
        self.background = Rectangle(pos=(self.pos[0], self.pos[1]), size=(self.width, self.height))
        # setup and draw all rectangles
        for sqr in self.game.view_board.squares:
            sqr_color = light if sqr.color == WHITE else dark
            # highlight the selected square
            if sqr == self.selected_square:
                sqr_color = self.theme.highlight
            Color(sqr_color[0], sqr_color[1], sqr_color[2], sqr_color[3], mode='rgba')
            draw_pos = [RANK_COUNT - (sqr.pos[0] + 1), FILE_COUNT - (sqr.pos[1] + 1)] if self.draw_flipped else sqr.pos
            sqr_pos = self.board_to_screen_pos(draw_pos)
            sqr.rect = Rectangle(pos=sqr_pos, size=(self.square_length, self.square_length))

    def render_possible_moves(self):
        if not self.show_possible_moves or self.selected_piece is None or self.game.game_type == GAME_TYPES['UNDEFINED']:
            return
        moves = self.selected_piece.get_possible_moves()
        for move in moves:
            sqr = self.game.board.get_square(move[0], move[1])
            draw_pos = [RANK_COUNT - (sqr.pos[0] + 1), FILE_COUNT - (sqr.pos[1] + 1)] \
                if self.draw_flipped else sqr.pos
            sqr_pos = self.board_to_screen_pos(draw_pos)
            # center the circle in the square
            circle_length = self.square_length / 3
            sqr_pos[0] = sqr_pos[0] + self.square_length / 2 - circle_length / 2
            sqr_pos[1] = sqr_pos[1] + self.square_length / 2 - circle_length / 2
            c = self.theme.contrast
            Color(c[0], c[1], c[2], c[3], mode='rgba')
            sqr.circle = Ellipse(pos=sqr_pos, size=[circle_length, circle_length])

    def flip(self):
        # toggle draw flipped variable
        self.draw_flipped = not self.draw_flipped
        # update the screen visually
        self.selected_piece = None
        self.selected_square = None
        self.render()

    def new_game(self):
        layout = BoxLayout(orientation='vertical')
        cancel_button = Button(text='Cancel')
        buttons = []
        for k, v in GAME_TYPES.items():
            if v >= 0:
                text = (k.replace('/', ' vs ').replace('+', ' + ')
                        .replace(' P', ' Player').replace('P ', 'Player '))
                button = StartButton(board_widget=self, text=f'{v}. {text}')
                layout.add_widget(button)
                buttons.append(button)
        layout.add_widget(cancel_button)
        self.popup = Popup(title='New Game', content=layout, auto_dismiss=False)
        cancel_button.bind(on_press=self.popup.dismiss)
        for button in buttons:
            button.popup = self.popup
        self.popup.open()

    def start_game(self, game_type):
        if game_type < 3:  # single-player chosen
            self.game.start_game(game_type)
            self.render()
        else:  # multi-player, initiate server communication
            pass

    def board_to_screen_pos(self, pos):
        x = self.square_length * pos[0] + self.margin + self.background.pos[0]
        y = self.square_length * pos[1] + self.margin + self.background.pos[1]
        return [x, y]

    def get_square(self, pos):
        # position is not valid
        if pos[0] < self.x or pos[0] > self.right or pos[1] < self.y or pos[1] > self.top:
            return None

        # calculate distance from pos
        def dist_from_pos(sqr):
            draw_pos = [RANK_COUNT - (sqr.pos[0] + 1), FILE_COUNT - (sqr.pos[1] + 1)] if self.draw_flipped else sqr.pos
            sqr_pos = self.board_to_screen_pos(draw_pos)
            # measure the distance from the center of the square
            sqr_pos[0] = sqr_pos[0] + self.square_length / 2
            sqr_pos[1] = sqr_pos[1] + self.square_length / 2
            return utils.dist(sqr_pos[0], sqr_pos[1], pos[0], pos[1])

        # sort the squares by their distance to the mouse
        self.game.view_board.squares.sort(key=lambda sqr: dist_from_pos(sqr))

        # return the closest square
        return self.game.view_board.squares[0]

    def on_touch_down(self, touch):
        # select a piece to move
        sqr = self.get_square(touch.pos)
        if sqr is None:
            return
        piece = self.game.view_board.get_piece(sqr.pos[0], sqr.pos[1])
        # only select the square if it has a piece on it
        if piece is not None:
            # can select any piece if game_type is undefined, otherwise can only
            # select a piece with the color of the person whose turn it is
            if self.game.game_type == GAME_TYPES['UNDEFINED'] or self.game.turn == piece.color:
                self.selected_square = sqr
                self.selected_piece = piece
                self.render()

    def on_touch_move(self, touch):
        # draw the piece by the mouse
        if self.selected_piece is not None:
            x = touch.pos[0] - self.square_length / 2
            y = touch.pos[1] - self.square_length / 2
            self.selected_piece.rect.pos = [x, y]

    def on_touch_up(self, touch):
        if self.selected_piece is not None:
            # return the piece to its original position
            # if move isn't valid
            sqr = self.selected_square
            hover_sqr = self.get_square(touch.pos)
            if hover_sqr is not None:
                sqr = hover_sqr
            result = self.game.move(self.selected_piece.pos, sqr.pos)
            self.selected_square = None
            self.selected_piece = None
            if self.auto_flip and result and self.game.game_type == GAME_TYPES['P/P']:
                self.flip()
            self.render()

    def next(self):
        self.game.next()
        self.render()

    def back(self):
        self.game.back()
        self.render()


class StartButton(Button):
    def __init__(self, board_widget, **kwargs):
        super(StartButton, self).__init__(**kwargs)
        self.game_type = -1
        self.board_widget = board_widget
        self.popup = None

    def on_press(self):
        self.game_type = int(self.text.split('.')[0])
        self.board_widget.start_game(self.game_type)
        self.popup.dismiss()


class BughouseBlitzApp(App):
    theme = THEMES['BLUE']

    def build(self):
        return FloatLayout()


if __name__ == '__main__':
    BughouseBlitzApp().run()
