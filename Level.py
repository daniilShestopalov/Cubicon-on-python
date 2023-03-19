class Level(object):

    def __init__(self, level_name: str):
        self.level_name = level_name
        self.field_int = []
        Level.read_level(self)

    def read_level(self):
        self.field_int.clear()
        file = open(self.level_name,"r")
        for s in file:
            self.field_int.append([int(x) for x in s.strip().split(" ")])
        file.close()

    def set_level_file_name(self, name: str):
        self.level_name = name
        Level.read_level(self)

    def get_level_name(self):
        return self.level_name

    def get_field(self):
        return self.field_int



