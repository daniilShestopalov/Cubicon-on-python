from State import State


class GameCell(object):

    def __init__(self, state: State, color: int):
        self.color = color
        self.state = state

    def get_color(self):
        return self.color

    def get_state(self):
        return self.state