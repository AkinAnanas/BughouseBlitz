from kivy.app import App
from kivy.core.image import Image
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget

from board import Board, RANK_COUNT, FILE_COUNT, WHITE
from theme import DEFAULT
import utils


class BoardWidget(Widget):
    def __init__(self, **kwargs):
        super(BoardWidget, self).__init__(**kwargs)
        self.board = Board()  # current board
        self.boards = []  # previous boards
        self.selected_square = None
        self.selected_piece = None
        self.theme = DEFAULT
        self.background = None
        self.draw_flipped = False
        self.margin = 0
        self.square_length = 0
        self.bind(size=self.render, pos=self.render)

    def test(self):
        data = str(self.board)
        self.set_board(Board.from_str(data))

    def set_board(self, board):
        self.board = board
        self.boards.clear()
        self.selected_square = None
        self.selected_piece = None
        self.render()

    def render(self, *args):
        self.canvas.clear()
        with self.canvas:
            # resize everything
            self.margin = self.width * .05
            self.square_length = (self.width - self.margin * 2) / RANK_COUNT
            self.render_squares()
            self.render_pieces()

    def render_pieces(self):
        # setup and draw all the pieces
        for piece in self.board.pieces:
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
        for sqr in self.board.squares:
            sqr_color = light if sqr.color == WHITE else dark
            # highlight the selected square
            if sqr == self.selected_square:
                sqr_color = self.theme.highlight
            Color(sqr_color[0], sqr_color[1], sqr_color[2], sqr_color[3], mode='rgba')
            draw_pos = [RANK_COUNT - (sqr.pos[0] + 1), FILE_COUNT - (sqr.pos[1] + 1)] if self.draw_flipped else sqr.pos
            sqr_pos = self.board_to_screen_pos(draw_pos)
            sqr.rect = Rectangle(pos=sqr_pos, size=(self.square_length, self.square_length))

    def render_possible_moves(self):
        pass

    def flip(self):
        # toggle draw flipped variable
        self.draw_flipped = not self.draw_flipped
        # update the screen visually
        self.selected_piece = None
        self.selected_square = None
        self.render()

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
        self.board.squares.sort(key=lambda sqr: dist_from_pos(sqr))

        # return the closest square
        return self.board.squares[0]

    def on_touch_down(self, touch):
        # select a piece to move
        sqr = self.get_square(touch.pos)
        if sqr is None:
            return
        piece = self.board.get_piece(sqr.pos[0], sqr.pos[1])
        # only select the square if it has a piece on it
        if piece is not None:
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
        # return the piece to its original position
        if self.selected_piece is not None:
            sqr = self.selected_square
            sqr_pos = self.board_to_screen_pos(sqr.pos)
            self.selected_piece.rect.pos = sqr_pos
            self.render()


class BughouseBlitzApp(App):
    def build(self):
        return FloatLayout()


if __name__ == '__main__':
    BughouseBlitzApp().run()
