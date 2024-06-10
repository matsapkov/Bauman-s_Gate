import random


class Unit:
    def __init__(self, name='name', hp=0, dp=0, mp=0, ap=0, ar=0, cost=0, TP=0, SP=0, RP=0, SC=None):
        self.__Name = name
        self.__hit_Points = hp
        self.__def_Points = dp
        self.__move_Points = mp
        self.__attack_Points = ap
        self.__attack_Range = ar
        self.__Cost = cost
        self.__tree_penalty = TP
        self.__swamp_penalty = SP
        self.__rock_penalty = RP
        self.__super_class = SC
        self.Position_i = None
        self.Position_j = None
        self.prev_positionI = 0
        self.prev_positionJ = 0

    def copy_from_alien(self, alien):
        self.__Name = alien._Alien__Name
        self.__hit_Points = alien._Alien__hit_Points
        self.__def_Points = alien._Alien__def_Points
        self.__move_Points = alien._Alien__move_Points
        self.__attack_Points = alien._Alien__attack_Points
        self.__attack_Range = alien._Alien__attack_Range
        self.__Cost = alien._Alien__Cost
        self.__tree_penalty = alien._Alien__tree_penalty
        self.__swamp_penalty = alien._Alien__swamp_penalty
        self.__rock_penalty = alien._Alien__rock_penalty
        self.__super_class = alien._Alien__super_class
        self.Position_i = alien.Position_i
        self.Position_j = alien.Position_j
        self.prev_positionI = 0
        self.prev_positionJ = 0

    def __getitem__(self, item):
        if (item == 'tree_penalty'):
            return self.__tree_penalty
        elif (item == 'swamp_penalty'):
            return self.__swamp_penalty
        elif (item == 'rock_penalty'):
            return self.__rock_penalty
        elif (item == 'Name'):
            return self.__Name
        elif (item == 'Cost'):
            return self.__Cost
        elif (item == 'Move_points'):
            return self.__move_Points
        elif (item == 'HP'):
            return self.__hit_Points
        elif (item == 'Attack_points'):
            return self.__attack_Points
        elif (item == 'range'):
            return self.__attack_Range
        elif (item == 'def'):
            return self.__def_Points
        elif (item == 'SC'):
            return self.__super_class

    @property
    def HP(self):
        return self.__hit_Points

    @HP.setter
    def HP(self, value):
        self.__hit_Points = value

    @property
    def RANGE(self):
        return self.__attack_Range

    @RANGE.setter
    def RANGE(self, value):
        self.__attack_Range = value

    @property
    def DEF(self):
        return self.__def_Points

    @DEF.setter
    def DEF(self, value):
        self.__def_Points = value

    @property
    def move_Points(self):
        return self.__move_Points

    @move_Points.setter
    def move_Points(self, value):
        self.__move_Points = value

    @property
    def attack_points(self):
        return self.__attack_Points

    @attack_points.setter
    def attack_points(self, value):
        self.__attack_Points = value

    def improve_stat(self, stat):
        if stat == 'hit_Points':
            self.__hit_Points += 1
        elif stat == 'def_Points':
            self.__def_Points += 1
        elif stat == 'move_Points':
            self.__move_Points += 1
        elif stat == 'attack_Points':
            self.__attack_Points += 1
        elif stat == 'attack_Range':
            self.__attack_Range += 1
        else:
            print("Недопустимая характеристика")

    def display_stats(self, player):
        print('----------------')
        for index, unit in player['units'].items():
            if unit == self:
                symbol = index

        print(f'Name: {self['Name']}\nHP: {self['HP']} \nSymbol: {symbol} \nAvailable move points: {self['Move_points']}\nDefPts: {self['def']}\nRange: {self['range']}\nAttackPoints: {self['Attack_points']}')
        print(self.Position_i, self.Position_j)
        print('----------------')
        return '\n'

    def save_coordinates(self):
        prevI = self.prev_positionI
        prevJ = self.prev_positionJ
        posI = self.Position_i
        posJ = self.Position_j
        data = [[prevI, prevJ],[posI, posJ]]
        return data

    def spawn_unit_from_academy(self, player, field):
        occupied_coords = set()
        units = player['units']
        self.Position_i = 0
        for unit in units.values():
            occupied_coords.add(unit.Position_j)
        while True:
            self.Position_j = random.randint(0, field.SIZE - 1)
            if self.Position_j not in occupied_coords:
                occupied_coords.add(self.Position_j)
                break
            else:
                continue

    def moving(self, Field):
        print("Введите координаты клетки, куда вы хотите переместить выбранный юнит (Пример: A5):")
        target_cell_str = input().strip().upper()

        column = target_cell_str[0]
        row = int(target_cell_str[1:])
        target_i = row
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        target_j = letters.find(column)
        self.prev_positionI, self.prev_positionJ = self.Position_i, self.Position_j
        target_cell = (target_i, target_j)
        if Field.is_cell_accessible(self, target_cell):
            self.Position_i, self.Position_j = target_i, target_j
            self.save_coordinates()
            print("Unit moved successfully.")
        else:
            print("Target cell is not accessible.")

    def attacking(self,bot, field, wizard):
        target_cell = input('Введите координату юнита для атаки: ' ).strip().upper()
        column = target_cell[0]
        row = int(target_cell[1:])
        target_i = row
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        target_j = letters.find(column)
        target_position = (target_i, target_j)
        start_position = (self.Position_i, self.Position_j)
        square_sum = (abs(target_position[1] - start_position[1])) ** 2 + (abs(target_position[0]) - start_position[0]) ** 2
        hypotenuse = square_sum ** 0.5

        choice = int(input('Если это чужой, введите 2, если это маг, введите 1, если это бот, введите 0: '))
        if choice == 0:
            if (self['range'] >= hypotenuse):
                for unit in bot.get_units():
                    data = unit.save_coordinates()
                    defender_pos = (data[1][0], data[1][1])
                    if (target_position == defender_pos):
                        bot.get_damage(self,unit, field)
            else:
                print('Attack is impossible')

        if (choice == 1):
            if (self['range'] >= hypotenuse):
                for unit in wizard.Wizards:
                    defender_pos = (wizard.Position_i,wizard.Position_j )
                    if (target_position == defender_pos):
                        print('Атака по магу реально работает')
                        unit.get_damage(self,  field)
            else:
                print('Attack is impossible')

        if choice == 2:
            if (self['range'] >= hypotenuse):
                for unit in wizard.Aliens:
                    data = unit.save_coordinates()
                    defender_pos = (data[1][0], data[1][1])
                    if (target_position == defender_pos):
                        unit.Get_damage(self, field, wizard)
            else:
                print('Attack is impossible')

    def get_damage(self, attacker, field, player):
        print(f'Your unit {self['Name']} was attacked by {attacker['Name']}!')
        damage_points = attacker['Attack_points']

        if (self['def'] != 0):
            while self['def'] != 0 and damage_points != 0:
                damage_points -= 1
                self._Unit__def_Points -= 1

        if (self.HP != 0 and damage_points != 0):
            while self.HP != 0 and damage_points != 0:
                damage_points -= 1
                self.HP -= 1
                if (self.HP == 0):
                    self.die(field, player)

    def die(self, field, player):
        print(f'Unit {self["Name"]} has died!')
        units = player['units']

        for key, value in units.items():
            if value == self:
                del units[key]
                break

        field.game_field[self.Position_i][self.Position_j] = field.sub_game_field[self.Position_i][self.Position_j]

