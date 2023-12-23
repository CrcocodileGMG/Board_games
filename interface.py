from checkers_base import CheckersFigure, Checker, CheckersKing, CheckersDesk
from constants import *
import pygame
from math import ceil


WHITE_COLOR = pygame.Color(255, 255, 255, 255)
GRAY_COLOR = pygame.Color(128, 128, 128, 255)
SELECT_CELL_COLOR = pygame.Color(0, 255, 0, 255)
SIZE = WIDTH, HEIGHT = 544, 544
FPS = 60
WHITE_KING, WHITE_CHECKER, BLACK_KING, BLACK_CHECKER = (pygame.image.load("WHITE_KING.png"),
                                                        pygame.image.load("WHITE_CHECKER.png"),
                                                        pygame.image.load("BLACK_KING.png"),
                                                        pygame.image.load("BLACK_CHECKER.png"))


class Cell:
    def __init__(self, indent_x, indent_y, side, color):
        self.indent_x, self.indent_y = indent_x, indent_y
        self.side = side
        self.color = color

    def get_inf(self):
        return self.indent_x, self.indent_y

    def update(self, figure=None):
        pygame.draw.rect(screen, self.color, (self.indent_x, self.indent_y, self.side, self.side))
        if figure is not None:
            screen.blit(figure, self.get_inf())

    def selected(self):
        pygame.draw.rect(screen, SELECT_CELL_COLOR, (self.indent_x, self.indent_y, self.side / 17, self.side))
        pygame.draw.rect(screen, SELECT_CELL_COLOR, (self.indent_x, self.indent_y, self.side, self.side / 17))
        pygame.draw.rect(screen, SELECT_CELL_COLOR, (self.indent_x + self.side * (16 / 17),
                                                     self.indent_y,
                                                     self.side / 17, self.side))
        pygame.draw.rect(screen, SELECT_CELL_COLOR, (self.indent_x,
                                                     self.indent_y + self.side * (16 / 17),
                                                     self.side, self.side / 17))


class Desk:
    def __init__(self, indent_x, indent_y, side):
        self.indent_x, self.indent_y = indent_x, indent_y
        self.side = side
        self.desk = []
        for y in range(7, -1, -1):
            line = []
            for x in range(8):
                line.append(Cell(self.indent_x + (self.get_cell_side()) * x,
                                 (self.indent_y + (self.get_cell_side()) * y), self.get_cell_side(),
                                 (WHITE_COLOR if (x + y) % 2 == 0 else GRAY_COLOR)))
            self.desk.append(line)

    def get_cell_side(self):
        return self.side / 8

    def get_cell(self, x, y):
        return self.desk[y - 1][x - 1]

    def cells_update(self):
        for y in range(1, 9):
            for x in range(1, 9):
                figure = checkers_desk.get_cell(x, y)
                if figure is None:
                    self.get_cell(x, y).update()
                else:
                    if isinstance(figure, Checker):
                        if figure.get_color() == WHITE:
                            self.get_cell(x, y).update(WHITE_CHECKER)
                        else:
                            self.get_cell(x, y).update(BLACK_CHECKER)
                    else:
                        if figure.get_color() == WHITE:
                            self.get_cell(x, y).update(WHITE_KING)
                        else:
                            self.get_cell(x, y).update(BLACK_KING)

    def cell_coordinate(self, x_pixels, y_pixels):
        return (ceil((x_pixels - self.indent_x) / (self.side / 8)),
                ceil((self.side - (y_pixels - self.indent_y)) / (self.side / 8)))


clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
desk = Desk(0, 0, side=544)
checkers_desk = CheckersDesk()
checkers_desk.standard_checkers()
desk.cells_update()
selected_cell = list()

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Ox, Oy = desk.cell_coordinate(event.pos[0], event.pos[1])
                if len(selected_cell) != 0:
                    if checkers_desk.check_move(selected_cell[0], selected_cell[1], Ox, Oy):
                        checkers_desk.move(selected_cell[0], selected_cell[1], Ox, Oy)
                        checkers_desk.change_color()
                    elif checkers_desk.check_attack(selected_cell[0], selected_cell[1], Ox, Oy):
                        checkers_desk.attack(selected_cell[0], selected_cell[1], Ox, Oy)
                        checkers_desk.change_color()
                    else:
                        print("Impossible move")
                    selected_cell = list()
                    desk.cells_update()
                    if checkers_desk.draw(checkers_desk.get_color()):
                        game = False
                        print("game end's with the draw")
                    if not checkers_desk.check_continue():
                        game = False
                        if checkers_desk.check_winner() == WHITE:
                            print("White won")
                        else:
                            print("Black won")
                else:
                    selected_figure = checkers_desk.get_cell(Ox, Oy)
                    if selected_figure is None:
                        print("The figure on this square was not found")
                    elif selected_figure.get_color() != checkers_desk.get_color():
                        print("You choose a figure with the wrong color")
                    else:
                        desk.get_cell(Ox, Oy).selected()
                        selected_cell = [Ox, Oy]
        if event.type == pygame.QUIT:
            game = False
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
