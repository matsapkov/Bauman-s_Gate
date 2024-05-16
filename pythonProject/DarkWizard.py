#ʘ - чужой
#ඞ - черный маг
from units import Unit
import random
import copy
class DarkWizard(Unit):
    def __init__(self, HP, dp, field):
        self.Aliens = []
        self.Wizards = []
        self.Captured_Player_Units = []
        self.Captured_Bot_Units = []
        self.Captured_Player_UnitsDict = {}
        self.Captured_Bot_UnitsDict = {}
        self.__hit_Points = HP
        self.__def_Points = dp
        self.turn = 0
        self.Position_i = field.SIZE // 2
        self.Position_j = field.SIZE // 2

    def __getitem__(self, item):
        if item == 'HP':
            return self.__hit_Points
        elif item == 'def':
            return self.__def_Points

    def __str__(self):
        pass

    def spawnAliens(self):
        occupied_cords = set()
        if self.turn % 2 == 0 and self.turn != 0:
            directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            alien = Alien(unit=Unit('name', 1,1,1,1,1,1,1,1,1))
            while True:
                direction = random.choice(directions)
                coords = (self.Position_i + direction[0], self.Position_j + direction[1])
                if coords not in occupied_cords:
                    occupied_cords.add(coords)
                    alien.Position_i = self.Position_i + direction[0]
                    alien.Position_j = self.Position_j + direction[1]
                    self.Aliens.append(alien)
                    break

    def Moving(self,field):
        if len(self.Aliens) != 0:
            for unit_ in self.Aliens:
                unit_.Go(field,  self)

        # if len(self.Captured_Player_Units) != 0:
        #     for unit_ in self.Captured_Player_Units:
        #         unit_.Go(field, self)
        #
        # if len(self.Captured_Bot_Units) != 0:
        #     for unit_ in self.Captured_Bot_Units:
        #         unit_.Go(field, self)

    def catch(self, player, bot):

        players_units_to_add = []
        bots_units_to_add = []

        player_units = player['units']
        bot_units = bot['dict_units']
        for alien in self.Aliens:
            for index, unit in player_units.items():
                if alien.Position_i == unit.Position_i and alien.Position_j == unit.Position_j:
                    print('Произошел захват юнита игрока')

                    copied_PlayerUnit = copy.deepcopy(unit)
                    self.Captured_Player_UnitsDict[index] = unit
                    # self.Aliens.append(Alien(copied_PlayerUnit))

                    players_units_to_add.append(Alien(copied_PlayerUnit))

                    # self.Captured_Player_Units.append(Alien(copied_PlayerUnit))

        self.Aliens.extend(players_units_to_add)

        for index, unit in self.Captured_Player_UnitsDict.items():
            if unit in player_units.values():
                del player_units[index]

        for alien in self.Aliens:
            for key, value in bot['dict_units'].items():
                if alien.Position_i == value.Position_i and alien.Position_j == value.Position_j:
                    print('Произошел захват юнита бота')



                    copied_BotUnit = copy.deepcopy(value)
                    self.Captured_Bot_UnitsDict[key] = value

                    bots_units_to_add.append(Alien(copied_BotUnit))

                    self.Aliens.append(Alien(copied_BotUnit))

        self.Aliens.extend(bots_units_to_add)

        for index, unit in self.Captured_Bot_UnitsDict.items():
            if unit in bot_units.values():
                del bot_units[index]

    def returning(self, player, bot, field):
        player_units = player['units']
        bot_units = bot['dict_units']
        for index, value in self.Captured_Player_UnitsDict.items():
            player_units[index] = value
            field.game_field[value.Position_i][value.Position_j] = index
        for index, value in self.Captured_Bot_UnitsDict.items():
            bot_units[index] = value
            field.game_field[value.Position_i][value.Position_j] = index

        self.Captured_Bot_UnitsDict.clear()
        self.Captured_Player_UnitsDict.clear()
        self.Captured_Player_Units.clear()
        self.Captured_Bot_Units.clear()

    def Die(self, field):
        print(f'----------DARK WIZARD HAS DIED----------')
        self.Wizards.clear()
        for unit in self.Aliens:
            unit.Die(field)
        self.Aliens.clear()
        field.game_field[self.Position_i][self.Position_j] = field.sub_game_field[self.Position_i][self.Position_j]


    def get_damage(self, attacker, field):
        damage_points = attacker['Attack_points']

        if (self['def'] != 0):
            while self['def'] != 0 and damage_points != 0:
                damage_points -= 1
                self.__def_Points -= 1

        if (self.HP != 0 and damage_points != 0):
            while self.HP != 0 and damage_points != 0:
                damage_points -= 1
                self.HP -= 1
                if (self.HP == 0):
                    self.Die(field)

    @property
    def TURN(self):
        return self.turn

    @TURN.setter
    def TURN(self, value):
        self.turn = value

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

class Alien(Unit):
    def __init__(self, unit):
        self.__Name = unit._Unit__Name
        self.__hit_Points = unit._Unit__hit_Points
        self.__def_Points = unit._Unit__def_Points
        self.__move_Points = unit._Unit__move_Points
        self.__attack_Points = unit._Unit__attack_Points
        self.__attack_Range = unit._Unit__attack_Range
        self.__Cost = unit._Unit__Cost
        self.__tree_penalty = unit._Unit__tree_penalty
        self.__swamp_penalty = unit._Unit__swamp_penalty
        self.__rock_penalty = unit._Unit__rock_penalty
        self.Position_i = unit.Position_i
        self.Position_j = unit.Position_j
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

    def Go(self, Field, wizard):
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        direction = random.choice(directions)

        if (Field.SIZE > self.Position_i + direction[0] >= 0) and (Field.SIZE > self.Position_j + direction[1] >= 0):
            print('Зашли в иф')
            print(f'Выпало направление ходьбы на {direction}')
            print(f'Текущие координаты {self.Position_i, self.Position_j}')
            print(f'Текущие координаты визарда {wizard.Position_i, wizard.Position_j}')
            print(f'НОВЫЕ КООРДИНАТЫ {self.Position_i + direction[0], self.Position_j + direction[1]}')
            if ((self.Position_i + direction[0] == wizard.Position_i) and (
                    self.Position_j + direction[1] == wizard.Position_j)):
                print('ПОЗИЦИЯ ВИЗАРДА И ЧУЖОГО СНОВА СОВПАЛА')
            if (self.Position_i + direction[0] != wizard.Position_i) or (self.Position_j + direction[1] != wizard.Position_j):
                print('ПОЗИЦИЯ ВИЗАРДА И ЧУЖОГО СНОВА НЕ СОВПАЛА')
                self.prev_positionI = self.Position_i
                self.prev_positionJ = self.Position_j
                self.Position_i = direction[0] + self.Position_i
                self.Position_j = direction[1] + self.Position_j

    def Get_damage(self, attacker, field, wizard):
        damage_points = attacker['Attack_points']

        if (self['def'] != 0):
            while self['def'] != 0 and damage_points != 0:
                damage_points -= 1
                self.__def_Points -= 1

        if (self.HP != 0 and damage_points != 0):
            while self.HP != 0 and damage_points != 0:
                damage_points -= 1
                self.HP -= 1
                if (self.HP == 0):
                    self.Die(field, wizard)

    def Die(self, field, wizard):
        print('Чужой умирает!')

        for index, value in enumerate(wizard.Aliens):
            if value == self:
                wizard.Aliens.pop(index)
                break

        field.game_field[self.Position_i][self.Position_j] = field.sub_game_field[self.Position_i][self.Position_j]

# alien = Alien(unit=Unit('name', 1,1,1,1,1,1,1,1,1))
# wizard = DarkWizard(100, 1, Field)
