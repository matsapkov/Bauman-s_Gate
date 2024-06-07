
class MapCreator:
    SIZE = 0
    __game_field = [[]]
    coordinates = {}
    __sub_game_field = [[]]
    obstacles = []

    def __init__(self, pickle_load):
        self.SIZE = pickle_load.SIZE
        self.game_field = pickle_load.game_field
        self.sub_game_field = pickle_load.sub_game_field
        self.obstacles = pickle_load.obstacles