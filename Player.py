from GameCell import GameCell
from State import State


class Player(GameCell):

    def __init__(self, x_pos: int, y_pos: int):
        super().__init__(State.PLAYER, -1)
        self.x_pos = x_pos
        self.y_pos = y_pos

    def get_x_pos(self):
        return self.x_pos

    def get_y_pos(self):
        return self.y_pos

    def set_x_pos(self, new_x: int):
        self.x_pos = new_x

    def set_y_pos(self, new_y: int):
        self.y_pos = new_y

