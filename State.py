import enum

class State(enum.Enum):
    WALL = 1
    CUBE = 2
    VOID = 0
    PLAYER = 3