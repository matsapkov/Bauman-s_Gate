class Unit:
    def __init__(self, name, hp, dp, mp, ap, ar, cost, TP, SP, RP):
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
        self.Position_i = 0
        self.Position_j = 0
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

    @property
    def HP(self):
        return self.__hit_Points
    @HP.setter
    def HP(self, value):
        self.__hit_Points = value

    @property
    def DEF(self):
        return self.__def_Points
    @DEF.setter
    def DEF(self, value):
        self.__def_Points = value

    def display_stats(self, player):
        print('----------------')
        print(f'Name: {self['Name']}\nHP: {self['HP']} \nSymbol: {player.get_units().index(self)} \nAvailable move points: {self['Move_points']}\nDefPts: {self['def']}\nRange: {self['range']}\nAttackPoints: {self['Attack_points']}')
        print('----------------')
        return '\n'

    def save_coordinates(self):
        prevI = self.prev_positionI
        prevJ = self.prev_positionJ
        posI = self.Position_i
        posJ = self.Position_j
        data = [[prevI, prevJ],[posI, posJ]]
        return data

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

    def attacking(self,bot, field):
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
        if (self['range'] >= hypotenuse):
            for unit in bot.get_units():
                data = unit.save_coordinates()
                defender_pos = (data[1][0], data[1][1])
                if (target_position == defender_pos):
                    bot.get_damage(self,unit, field)
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
        units = player.get_units()
        for i in range(len(units)):
            if units[i] == self:
                units.pop(i)
                break
        field.game_field[self.Position_i][self.Position_j] = field.sub_game_field[self.Position_i][self.Position_j]


