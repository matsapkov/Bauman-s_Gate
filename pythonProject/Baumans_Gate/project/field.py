import random
from collections import deque
class Field:


    SIZE = 0
    __game_field = [[]]
    coordinates = {}
    __sub_game_field = [[]]
    obstacles = []
    def __init__(self, size=0, GAME_FIELD=None, SUB_GAME_FIELD=None):
        self.SIZE = size
        if GAME_FIELD is None:
            GAME_FIELD = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        if SUB_GAME_FIELD is None:
            SUB_GAME_FIELD = [[0 for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        self.game_field = GAME_FIELD
        self.sub_game_field = SUB_GAME_FIELD
        self.coordinates = {}


    def copy_from_pickle(self, pickled_field):
        self.SIZE = pickled_field.SIZE
        self.game_field = pickled_field.game_field
        self.sub_game_field = pickled_field.sub_game_field
        self.obstacles = pickled_field.obstacles

    def fill_field(self):
        print(f'Размер поля {len(self.game_field)}')
        obstacle_probability = [0.1, 0.2, 0.3]
        for i in range(1, self.SIZE - 1):
            for j in range(self.SIZE):
                rand = random.random()
                if rand < obstacle_probability[0]:
                    self.game_field[i][j] = '^'             #дерево
                    self.sub_game_field[i][j] = '^'
                elif rand < obstacle_probability[1]:
                    self.game_field[i][j] = '#'           #болото
                    self.sub_game_field[i][j] = '#'
                elif rand < obstacle_probability[2]:
                    self.game_field[i][j] = '{'            #холм
                    self.sub_game_field[i][j] = '{'
                else:
                    self.game_field[i][j] = '*'           #обычная равнина
                    self.sub_game_field[i][j] = '*'

        for j in range(self.SIZE):
            self.game_field[0][j] = '*'
            self.game_field[self.SIZE - 1][j] = '*'
            self.sub_game_field[0][j] = '*'
            self.sub_game_field[self.SIZE - 1][j] = '*'


    def create_coordinates(self):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for i in range(self.SIZE):
            self.coordinates[i] = {}
            for j in range(self.SIZE):
                self.coordinates[i][j] = f'{letters[j]}{i}'

    def print_field(self, game_field):
        for row in game_field:
            print(' '.join(map(str, row)))

    def print_coordinates(self):

        for i in range(self.SIZE):
            for j in range( self.SIZE):
                print(self.coordinates[i][j], end='\t')
            print()

    def spawn_units(self, Player):
        occupied_coordinates = set()
        units = Player['units']
        for index, unit in units.items():
            unit.Position_i = 0
            while True:
                unit.Position_j = random.randint(0, self.SIZE - 1)
                if (unit.Position_i, unit.Position_j) not in occupied_coordinates:
                    occupied_coordinates.add((unit.Position_i, unit.Position_j))
                    self.game_field[unit.Position_i][unit.Position_j] = index  # Использование счетчика индекса
                    break

    def spawn_WIZARD(self, Wizard):
        self.game_field[Wizard.Position_i][Wizard.Position_j] = 'ඞ'

    def spawn_BOTunits(self, bot):
        occupied_coordinates = set()
        units = bot['dict_units']
        for letter, unit in units.items():
            unit.Position_i = self.SIZE - 1
            while True:
                unit.Position_j = random.randint(0, self.SIZE - 1)  # Случайная координата по горизонтали
                if unit.Position_j not in occupied_coordinates:
                    occupied_coordinates.add(unit.Position_j)
                    self.game_field[unit.Position_i][unit.Position_j] = letter
                    break

    def shortest_path_with_penalty(self, start, end, unit):
        visited = set()
        queue = deque([(start, [], 0)])
        while queue:
            current, path, penalty = queue.popleft()
            if current == end:
                return path + [current], penalty  # Возвращаем путь и суммарный штраф
            if current in visited:
                continue
            visited.add(current)
            for neighbor in self.get_neighbors(current[0], current[1]):
                target_i, target_j = neighbor
                terrain_type = self.game_field[target_i][target_j]
                cell_penalty = 1  # Штраф по умолчанию для обычной клетки "*"
                if terrain_type == '#':  # Болото
                    cell_penalty = unit['swamp_penalty']
                elif terrain_type == '^':  # Дерево
                    cell_penalty = unit['tree_penalty']
                elif terrain_type == '{':  # Холм
                    cell_penalty = unit['rock_penalty']
                if terrain_type in self.obstacles:
                    for obstacle in self.obstacles:
                        if terrain_type == obstacle.symbol:
                            if unit['SC'] == 'on_foot':
                                cell_penalty = obstacle.unit_on_foot_penalty
                            if unit['SC'] == 'cavalry':
                                cell_penalty = obstacle.unit_on_cavalry_penalty
                            if unit['SC'] == 'shooting':
                                cell_penalty = obstacle.unit_shooting_penalty
                new_penalty = penalty + cell_penalty
                queue.append((neighbor, path + [current], new_penalty))
        return None, 0

    def is_cell_accessible(self, unit, target_cell):
        start_position = (unit.Position_i, unit.Position_j)
        path, penalty = self.shortest_path_with_penalty(start_position, target_cell, unit)
        #print(f'Кратчайший путь до клетки {path} с весом перемещения {penalty}')
        if path is not None:
            remaining_move_points = unit['Move_points'] - penalty

            return remaining_move_points >= 0
        else:
            return False

    def get_neighbors(self, i, j):
        neighbors = []
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dx, dy in directions:
            new_i, new_j = i + dx, j + dy
            if 0 <= new_i < self.SIZE and 0 <= new_j < self.SIZE:
                neighbors.append((new_i, new_j))
        return neighbors

    @property
    def get_sub_game_field(self):
        return self.sub_game_field

    def update_field(self, Player, Bot, DarkWizard):
        for index, unit in Player['units'].items():
            data = unit.save_coordinates()
            if([data[1][0],data[1][1]] != [data[0][0],data[0][1]]):
                self.game_field[data[1][0]][data[1][1]] = index
                self.game_field[data[0][0]][data[0][1]] = self.sub_game_field[data[0][0]][data[0][1]]
        for letter, Unitt in Bot['dict_units'].items():
            data = Unitt.save_coordinates()
            if([data[1][0],data[1][1]] != [data[0][0],data[0][1]]):
                self.game_field[data[1][0]][data[1][1]] = letter
                self.game_field[data[0][0]][data[0][1]] = self.sub_game_field[data[0][0]][data[0][1]]
        for unit_ in DarkWizard.Aliens:
            self.game_field[unit_.Position_i][unit_.Position_j] = 'ʘ'
            self.game_field[unit_.prev_positionI][unit_.prev_positionJ] = self.sub_game_field[unit_.prev_positionI][unit_.prev_positionJ]