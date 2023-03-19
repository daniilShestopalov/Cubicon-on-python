import enum
import copy

import ColorNotFound
from GameCell import GameCell
from Level import Level
from Player import Player
from State import State


class GameState(enum.Enum):
    NOT_STARTED = 0
    PLAYING = 1
    WIN = 2

class Game(object):

    def __init__(self, color_count: int):
        self.state = GameState.NOT_STARTED
        self.is_line = []
        self.color_count = color_count
        self.num_of_cubes_by_colors = []
        self.field = []

    def new_game(self, level: Level, player: Player):
        self.is_line.clear()
        self.num_of_cubes_by_colors.clear()

        self.is_line.extend([True] * self.color_count)
        self.num_of_cubes_by_colors.extend([0] * self.color_count)
        field_int = copy.deepcopy(level.get_field())
        self.fill_field(field_int, player)
        self.state = GameState.PLAYING

    def fill_field(self, field_int: list, player: Player):
        length_of_field_int = len(field_int)
        length_of_field_int_zero = len(field_int[0])
        self.field.clear()
        row = []
        for r in range(length_of_field_int):
            cell = None
            for c in range(length_of_field_int_zero):
                if field_int[r][c] == 11:
                    player.set_x_pos(c)
                    player.set_y_pos(r)
                    cell = player
                else:
                    if field_int[r][c] > 1:
                        if field_int[r][c] - 2 > self.color_count:
                            raise ColorNotFound.ColorNotFoundException()
                        cell = GameCell(State.CUBE, field_int[r][c] - 2)
                        self.num_of_cubes_by_colors[field_int[r][c] - 2] += 1
                        self.is_line[field_int[r][c] - 2] = False
                if field_int[r][c] == 0:
                    cell = GameCell(State.WALL, -1)
                if field_int[r][c] == 1:
                    cell = GameCell(State.VOID, -1)
                row.append(cell)
            self.field.append(copy.deepcopy(row))
            row.clear()

    def is_win(self):
        line = 0
        for l in self.is_line:
            if l:
                line += 1
        if line == len(self.num_of_cubes_by_colors):
            self.state = GameState.WIN
        else:
            self.state = GameState.PLAYING

    def get_state(self):
        return self.state

    def get_row_count(self):
        if self.field is None:
            return 0
        else:
            return len(self.field)

    def get_col_count(self):
        if self.field is None:
            return 0
        else:
            return len(self.field[0])

    def get_cell(self, row: int, col: int):
        if self.field is None or row < 0 or row >= self.get_row_count() or col < 0 or col >= self.get_col_count():
            return None
        return self.field[row][col]

    def right_move(self, player_pos_x: int, player_pos_y: int, player: Player):
        if self.state != GameState.PLAYING:
            return
        move_x = player_pos_x + 1
        move_y = player_pos_y
        wall_behind_cube_x = move_x + 1
        wall_behind_cube_y = move_y
        self.move(player, player_pos_x, player_pos_y, move_x, move_y, wall_behind_cube_x, wall_behind_cube_y)
        self.is_win()

    def left_move(self, player_pos_x: int, player_pos_y: int, player: Player):
        if self.state != GameState.PLAYING:
            return
        move_x = player_pos_x - 1
        move_y = player_pos_y
        wall_behind_cube_x = move_x - 1
        wall_behind_cube_y = move_y
        self.move(player, player_pos_x, player_pos_y, move_x, move_y, wall_behind_cube_x, wall_behind_cube_y)
        self.is_win()

    def up_move(self, player_pos_x: int, player_pos_y: int, player: Player):
        if self.state != GameState.PLAYING:
            return
        move_x = player_pos_x
        move_y = player_pos_y - 1
        wall_behind_cube_x = move_x
        wall_behind_cube_y = move_y - 1
        self.move(player, player_pos_x, player_pos_y, move_x, move_y, wall_behind_cube_x, wall_behind_cube_y)
        self.is_win()

    def down_move(self, player_pos_x: int, player_pos_y: int, player: Player):
        if self.state != GameState.PLAYING:
            return
        move_x = player_pos_x
        move_y = player_pos_y + 1
        wall_behind_cube_x = move_x
        wall_behind_cube_y = move_y + 1
        self.move(player, player_pos_x, player_pos_y, move_x, move_y, wall_behind_cube_x, wall_behind_cube_y)
        self.is_win()

    def move(self, player: Player, player_pos_x: int, player_pos_y: int, move_x: int, move_y: int,
             wall_behind_cube_x: int, wall_behind_cube_y:int):

        if self.field[move_y][move_x].get_state() == State.WALL:
            return
        if self.field[wall_behind_cube_y][wall_behind_cube_x].get_state() == State.WALL and \
                self.field[move_y][move_x].get_state() == State.CUBE:
            return
        if self.field[wall_behind_cube_y][wall_behind_cube_x].get_state() == State.CUBE and \
                self.field[move_y][move_x].get_state() == State.CUBE:
            return
        if self.field[move_y][move_x].get_state() == State.CUBE:
            self.field[move_y][move_x], self.field[wall_behind_cube_y][wall_behind_cube_x] =\
                self.field[wall_behind_cube_y][wall_behind_cube_x], self.field[move_y][move_x]
            self.is_cube_forming_line(wall_behind_cube_x, wall_behind_cube_y)

        self.field[player_pos_y][player_pos_x], self.field[move_y][move_x] = \
            self.field[move_y][move_x], self.field[player_pos_y][player_pos_x]
        player.set_x_pos(move_x)
        player.set_y_pos(move_y)

    def is_cube_forming_line(self, cube_pos_x: int, cube_pos_y: int):
        color = self.field[cube_pos_y][cube_pos_x].get_color()
        if color == -1:
            return
        num_of_cubes = self.num_of_cubes_by_colors[color]
        if self.is_cube_forming_line_by_x(cube_pos_y, cube_pos_x, color, num_of_cubes) or \
                              self.is_cube_forming_line_by_y(cube_pos_y, cube_pos_x, color, num_of_cubes):
            self.is_line[color] = True

    def is_cube_forming_line_by_x(self, cube_pos_y: int, cube_pos_x: int, color: int, num_of_cubes: int):
        count_of_cubes = 1
        if self.field[cube_pos_y][cube_pos_x - 1].get_color() == color and \
                self.field[cube_pos_y][cube_pos_x - 1].get_state() == State.CUBE:
            count_of_cubes += 1
            for i in range(2, num_of_cubes):
                if self.field[cube_pos_y][cube_pos_x - i].get_color() == color and \
                        self.field[cube_pos_y][cube_pos_x - i].get_state() == State.CUBE:
                    count_of_cubes += 1

        if self.field[cube_pos_y][cube_pos_x + 1].get_color() == color and \
                self.field[cube_pos_y][cube_pos_x + 1].get_state() == State.CUBE:
            count_of_cubes += 1
            for i in range(2, num_of_cubes):
                if self.field[cube_pos_y][cube_pos_x + i].get_color() == color and \
                        self.field[cube_pos_y][cube_pos_x + i].get_state() == State.CUBE:
                    count_of_cubes += 1
        return num_of_cubes == count_of_cubes

    def is_cube_forming_line_by_y(self, cube_pos_y, cube_pos_x, color, num_of_cubes):
        count_of_cubes = 1

        if self.field[cube_pos_y + 1][cube_pos_x].get_color() == color and \
                self.field[cube_pos_y + 1][cube_pos_x].get_state() == State.CUBE:
            count_of_cubes += 1
            for i in range(2, num_of_cubes):
                if self.field[cube_pos_y + i][cube_pos_x].get_color() == color and \
                        self.field[cube_pos_y + i][cube_pos_x].get_state() == State.CUBE:
                    count_of_cubes += 1

        if self.field[cube_pos_y - 1][cube_pos_x].get_color() == color and \
                self.field[cube_pos_y - 1][cube_pos_x].get_state() == State.CUBE:
            count_of_cubes += 1
            for i in range(2, num_of_cubes):
                if self.field[cube_pos_y - i][cube_pos_x].get_color() == color and \
                        self.field[cube_pos_y - i][cube_pos_x].get_state() == State.CUBE:
                    count_of_cubes += 1
        return num_of_cubes == count_of_cubes