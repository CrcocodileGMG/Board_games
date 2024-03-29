from functions import cell_to_coordinates, coordinates_to_cell
from constants import *


class CheckersFigure:
    """
        Args:
            color (bool): input format: True(white), False(black)
    """

    def __init__(self, color: bool):
        self.__color = color

    def get_color(self):
        return self.__color

    def get_char(self):
        return self.__str__()

    def __str__(self) -> str:
        """
            Returns:
                figure display (str)
        """

        if self.__color:
            return self.char_black
        return self.char_white

    def __repr__(self):
        return self.__str__()


class Checker(CheckersFigure):
    def __init__(self, color):
        super().__init__(color)
        self.char_white = "⛀"
        self.char_black = "⛂"

    def check_move(self, x1, y1, x2, y2):
        if self.get_color() == WHITE:
            if abs(x2 - x1) == 1 and y2 - y1 == 1:
                return True
        else:
            if abs(x2 - x1) == 1 and y2 - y1 == -1:
                return True
        return False

    @staticmethod
    def check_attack(x1, y1, x2, y2):
        if abs(x2 - x1) == abs(y2 - y1) == 2:
            return True
        return False


class CheckersKing(CheckersFigure):
    def __init__(self, color):
        super().__init__(color)
        self.char_white = "⛁"
        self.char_black = "⛃"

    @staticmethod
    def check_move(x1, y1, x2, y2):
        if abs(x2 - x1) == abs(y2 - y1) and x1 != x2 and y1 != y2:
            return True
        return False

    @staticmethod
    def check_attack(x1, y1, x2, y2):
        if abs(x2 - x1) == abs(y2 - y1) > 1:
            return True
        return False


class CheckersDesk:
    def __init__(self):
        self.desk = [[None for _ in range(8)] for _ in range(8)]
        self.__move_color = WHITE

    def __str__(self) -> str:
        output = str()
        for i in range(8):
            output += str(8 - i) + " "
            for j in range(8):
                figure = self.desk[7 - i][j]
                if figure is None:
                    output += "※ "
                    continue
                output += figure.get_char() + " "
            output = output[:-1]
            output += "\n"
        output += "   A   B   C  D   E   F  G   H"
        return output

    def standard_checkers(self):
        self.desk = [[Checker(WHITE), None, Checker(WHITE), None, Checker(WHITE), None, Checker(WHITE), None],
                     [None, Checker(WHITE), None, Checker(WHITE), None, Checker(WHITE), None, Checker(WHITE)],
                     [Checker(WHITE), None, Checker(WHITE), None, Checker(WHITE), None, Checker(WHITE), None],
                     [None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None],
                     [None, Checker(BLACK), None, Checker(BLACK), None, Checker(BLACK), None, Checker(BLACK)],
                     [Checker(BLACK), None, Checker(BLACK), None, Checker(BLACK), None, Checker(BLACK), None],
                     [None, Checker(BLACK), None, Checker(BLACK), None, Checker(BLACK), None, Checker(BLACK)]]

    def change_color(self):
        self.__move_color = not self.__move_color

    def get_color(self) -> bool:
        return self.__move_color

    def add(self, x, y, figure):
        self.desk[y - 1][x - 1] = figure

    def remove(self, x, y):
        self.desk[y - 1][x - 1] = None

    def get_cell(self, x, y):
        return self.desk[y - 1][x - 1]

    def move(self, x1, y1, x2, y2):
        if isinstance(self.get_cell(x1, y1), Checker) and self.get_cell(x1, y1).get_color() == WHITE and y2 == 8:
            self.desk[y2 - 1][x2 - 1] = CheckersKing(WHITE)
            self.desk[y1 - 1][x1 - 1] = None
        elif isinstance(self.get_cell(x1, y1), Checker) and self.get_cell(x1, y1).get_color() == BLACK and y2 == 1:
            self.desk[y2 - 1][x2 - 1] = CheckersKing(BLACK)
            self.desk[y1 - 1][x1 - 1] = None
        else:
            self.desk[y2 - 1][x2 - 1] = self.desk[y1 - 1][x1 - 1]
            self.desk[y1 - 1][x1 - 1] = None

    def attack(self, x1, y1, x2, y2):
        if isinstance(self.get_cell(x1, y1), Checker) and self.get_cell(x1, y1).get_color() == WHITE and y2 == 8:
            self.desk[y2 - 1][x2 - 1] = CheckersKing(WHITE)
            self.desk[y1 - 1][x1 - 1] = None
        elif isinstance(self.get_cell(x1, y1), Checker) and self.get_cell(x1, y1).get_color() == BLACK and y2 == 1:
            self.desk[y2 - 1][x2 - 1] = CheckersKing(BLACK)
            self.desk[y1 - 1][x1 - 1] = None
        else:
            self.desk[y2 - 1][x2 - 1] = self.desk[y1 - 1][x1 - 1]
            self.desk[y1 - 1][x1 - 1] = None
        self.clear_line(x1, y1, x2, y2)

    def clear_line(self, x1, y1, x2, y2):
        if x1 < x2 and y1 < y2:
            for i in range(1, x2 - x1):
                if self.get_cell(x1 + i, y1 + i) is not None:
                    self.remove(x1 + i, y1 + i)
                    break
        elif x1 < x2 and y2 < y1:
            for i in range(1, x2 - x1):
                if self.get_cell(x1 + i, y1 - i) is not None:
                    self.remove(x1 + i, y1 - i)
                    break
        elif x2 < x1 and y2 < y1:
            for i in range(1, abs(x2 - x1)):
                if self.get_cell(x1 - i, y1 - i) is not None:
                    self.remove(x1 - i, y1 - i)
                    break
        elif x2 < x1 and y1 < y2:
            for i in range(1, abs(x2 - x1)):
                if self.get_cell(x1 - i, y1 + i) is not None:
                    self.remove(x1 - i, y1 + i)
                    break

    def check_move(self, x1, y1, x2, y2):
        if self.get_cell(x1, y1).check_move(x1, y1, x2, y2):
            if x1 < x2 and y1 < y2:
                for i in range(1, x2 - x1 + 1):
                    if self.get_cell(x1 + i, y1 + i) is not None:
                        return False
                return True
            elif x1 < x2 and y2 < y1:
                for i in range(1, x2 - x1 + 1):
                    if self.get_cell(x1 + i, y1 - i) is not None:
                        return False
                return True
            elif x2 < x1 and y2 < y1:
                for i in range(1, abs(x2 - x1) + 1):
                    if self.get_cell(x1 - i, y1 - i) is not None:
                        return False
                return True
            elif x2 < x1 and y1 < y2:
                for i in range(1, abs(x2 - x1) + 1):
                    if self.get_cell(x1 - i, y1 + i) is not None:
                        return False
                return True
        return False

    def check_attack(self, x1, y1, x2, y2):
        if self.get_cell(x1, y1).check_attack(x1, y1, x2, y2):
            figure_count_line = 0
            if x1 < x2 and y1 < y2:
                for i in range(1, x2 - x1):
                    if self.get_cell(x1 + i, y1 + i) is not None:
                        if self.get_cell(x1, y1).get_color() != self.get_cell(x1 + i, y1 + i).get_color():
                            figure_count_line += 1
                        else:
                            return False
                    if figure_count_line == 2:
                        return False
            elif x1 < x2 and y2 < y1:
                for i in range(1, x2 - x1):
                    if self.get_cell(x1 + i, y1 - i) is not None:
                        if self.get_cell(x1, y1).get_color() != self.get_cell(x1 + i, y1 - i).get_color():
                            figure_count_line += 1
                        else:
                            return False
                    if figure_count_line == 2:
                        return False
            elif x2 < x1 and y2 < y1:
                for i in range(1, abs(x2 - x1)):
                    if self.get_cell(x1 - i, y1 - i) is not None:
                        if self.get_cell(x1, y1).get_color() != self.get_cell(x1 - i, y1 - i).get_color():
                            figure_count_line += 1
                        else:
                            return False
                    if figure_count_line == 2:
                        return False
            elif x2 < x1 and y1 < y2:
                for i in range(1, abs(x2 - x1)):
                    if self.get_cell(x1 - i, y1 + i) is not None:
                        if self.get_cell(x1, y1).get_color() != self.get_cell(x1 - i, y1 + i).get_color():
                            figure_count_line += 1
                        else:
                            return False
                    if figure_count_line == 2:
                        return False
            if figure_count_line == 1 and self.get_cell(x2, y2) is None:
                return True
        return False

    def check_continue(self):
        white_figure = False
        black_figure = False
        for line in self.desk:
            for cell in line:
                if cell is not None:
                    if cell.get_color():
                        white_figure = True
                    elif not cell.get_color():
                        black_figure = True
                    if white_figure and black_figure:
                        return True
        return False

    def check_can_move_down(self, x, y, color):
        if y != 1:
            if x == 1:
                if self.get_cell(x + 1, y - 1) is None:
                    return True
                elif y != 2:
                    if self.get_cell(x + 1, y - 1).get_color() == (not color) and self.get_cell(x + 2, y - 2) is None:
                        return True
            elif x == 2:
                if self.get_cell(x - 1, y - 1) is None or self.get_cell(x + 1, y - 1) is None:
                    return True
                elif y != 2:
                    if self.get_cell(x + 1, y - 1).get_color() == (not color) and self.get_cell(x + 2, y - 2) is None:
                        return True
            elif x == 7:
                if self.get_cell(x - 1, y - 1) is None or self.get_cell(x + 1, y - 1) is None:
                    return True
                elif y != 2:
                    if self.get_cell(x - 1, y - 1).get_color() == (not color) and self.get_cell(x - 2, y - 2) is None:
                        return True
            elif x == 8:
                if self.get_cell(x - 1, y - 1) is None:
                    return True
                elif y != 2:
                    if self.get_cell(x - 1, y - 1).get_color() == (not color) and self.get_cell(x - 2, y - 2) is None:
                        return True
            else:
                if self.get_cell(x - 1, y - 1) is None or self.get_cell(x + 1, y - 1) is None:
                    return True
                elif y != 2:
                    if ((self.get_cell(x + 1, y - 1).get_color() == (not color) and
                         self.get_cell(x + 2, y - 2) is None) or
                            (self.get_cell(x - 1, y - 1).get_color() == (not color) and
                             self.get_cell(x - 2, y - 2) is None)):
                        return True
        return False

    def check_can_move_up(self, x, y, color):
        if y != 8:
            if x == 1:
                if self.get_cell(x + 1, y + 1) is None:
                    return True
                elif y != 7:
                    if self.get_cell(x + 1, y + 1).get_color() == (not color) and self.get_cell(x + 2, y + 2) is None:
                        return True
            elif x == 2:
                if self.get_cell(x - 1, y + 1) is None or self.get_cell(x + 1, y + 1) is None:
                    return True
                elif y != 7:
                    if self.get_cell(x + 1, y + 1).get_color() == (not color) and self.get_cell(x + 2, y + 2) is None:
                        return True
            elif x == 7:
                if self.get_cell(x - 1, y + 1) is None or self.get_cell(x + 1, y + 1) is None:
                    return True
                elif y != 7:
                    if self.get_cell(x - 1, y + 1).get_color() == (not color) and self.get_cell(x - 2, y + 2) is None:
                        return True
            elif x == 8:
                if self.get_cell(x - 1, y + 1) is None:
                    return True
                elif y != 7:
                    if self.get_cell(x - 1, y + 1).get_color() == (not color) and self.get_cell(x - 2, y + 2) is None:
                        return True
            else:
                if self.get_cell(x - 1, y + 1) is None or self.get_cell(x + 1, y + 1) is None:
                    return True
                elif y != 7:
                    if ((self.get_cell(x + 1, y + 1).get_color() == (not color) and
                         self.get_cell(x + 2, y + 2) is None) or
                        (self.get_cell(x - 1, y + 1).get_color() == (not color) and
                         self.get_cell(x - 2, y + 2) is None)):
                        return True
        return False

    def check_can_attack_right_up(self, x, y):
        if x <= 6 and y <= 6:
            if isinstance(self.get_cell(x, y), Checker):
                if self.get_cell(x + 1, y + 1) is not None:
                    if (self.get_cell(x + 1, y + 1).get_color() != self.get_cell(x, y).get_color() and
                            self.get_cell(x + 2, y + 2) is None):
                        return True
            else:
                enemy_figure_counter = 0
                for i in range(1, min(8 - x, 8 - y) + 1):
                    if self.get_cell(x + i, y + i) is not None:
                        if self.get_cell(x + i, y + i).get_color() != self.get_cell(x, y).get_color():
                            enemy_figure_counter += 1
                        else:
                            return False
                    elif enemy_figure_counter == 1:
                        return True
                    elif enemy_figure_counter > 1:
                        return False
        return False

    def check_can_attack_left_up(self, x, y):
        if x >= 3 and y <= 6:
            if isinstance(self.get_cell(x, y), Checker):
                if self.get_cell(x - 1, y + 1) is not None:
                    if (self.get_cell(x - 1, y + 1).get_color() != self.get_cell(x, y).get_color() and
                            self.get_cell(x - 2, y + 2) is None):
                        return True
            else:
                enemy_figure_counter = 0
                for i in range(1, min(x - 1, 8 - y) + 1):
                    if self.get_cell(x - i, y + i) is not None:
                        if self.get_cell(x - i, y + i).get_color() != self.get_cell(x, y).get_color():
                            enemy_figure_counter += 1
                        else:
                            return False
                    elif enemy_figure_counter == 1:
                        return True
                    elif enemy_figure_counter > 1:
                        return False
        return False

    def check_can_attack_right_down(self, x, y):
        if x <= 6 and y >= 3:
            if isinstance(self.get_cell(x, y), Checker):
                if self.get_cell(x + 1, y - 1) is not None:
                    if (self.get_cell(x + 1, y - 1).get_color() != self.get_cell(x, y).get_color() and
                            self.get_cell(x + 2, y - 2) is None):
                        return True
            else:
                enemy_figure_counter = 0
                for i in range(1, min(8 - x, y - 1) + 1):
                    if self.get_cell(x + i, y - i) is not None:
                        if self.get_cell(x + i, y - i).get_color() != self.get_cell(x, y).get_color():
                            enemy_figure_counter += 1
                        else:
                            return False
                    elif enemy_figure_counter == 1:
                        return True
                    elif enemy_figure_counter > 1:
                        return False
        return False

    def check_can_attack_left_down(self, x, y):
        if x >= 3 and y >= 3:
            if isinstance(self.get_cell(x, y), Checker):
                if self.get_cell(x - 1, y - 1) is not None:
                    if (self.get_cell(x - 1, y - 1).get_color() != self.get_cell(x, y).get_color() and
                            self.get_cell(x - 2, y - 2) is None):
                        return True
            else:
                enemy_figure_counter = 0
                for i in range(1, min(x - 1, y - 1) + 1):
                    if self.get_cell(x - i, y - i) is not None:
                        if self.get_cell(x - i, y - i).get_color() != self.get_cell(x, y).get_color():
                            enemy_figure_counter += 1
                        else:
                            return False
                    elif enemy_figure_counter == 1:
                        return True
                    elif enemy_figure_counter > 1:
                        return False
        return False

    def check_can_move(self, x, y):
        if isinstance(self.get_cell(x, y), Checker):
            if self.get_cell(x, y).get_color() == WHITE:
                return self.check_can_move_up(x, y, WHITE)
            elif self.get_cell(x, y).get_color() == BLACK:
                return self.check_can_move_down(x, y, BLACK)
        return (self.check_can_move_up(x, y, self.get_cell(x, y).get_color()) or
                self.check_can_move_down(x, y, self.get_cell(x, y).get_color()))

    def check_can_attack(self, x, y):
        return (self.check_can_attack_right_up(x, y) or self.check_can_attack_left_up(x, y) or
                self.check_can_attack_right_down(x, y) or self.check_can_attack_left_down(x, y))

    def must_attack(self, color):
        for y in range(1, 9):
            for x in range(1, 9):
                if self.get_cell(x, y) is not None and self.get_cell(x, y).get_color() == color:
                    if self.check_can_attack(x, y):
                        return True
        return False

    def draw(self, color):
        for y in range(1, 9):
            for x in range(1, 9):
                if self.get_cell(x, y) is not None and self.get_cell(x, y).get_color() == color:
                    if self.check_can_move(x, y):
                        return False
        return True

    def check_winner(self):
        for line in self.desk:
            for cell in line:
                if cell is not None:
                    if cell.get_color():
                        return True
                    else:
                        return False

    def is_empty(self):
        if self.desk == [[None for _ in range(8)] for _ in range(8)]:
            return True
        return False
