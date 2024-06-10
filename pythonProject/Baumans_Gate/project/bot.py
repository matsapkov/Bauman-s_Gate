from Baumans_Gate.project.player import Player
import random
from Baumans_Gate.project.units import Unit

Swordsman = Unit('Swordsman', 50, 8,3, 5,1, 10, 1,1.5,2)
Horseman = Unit('Horseman', 30, 7, 6,5,1,20,1,1.5,2)
Archer = Unit('Archer', 30,8,2,6,5,15,1,1.5,2)

class Bot(Player, Unit):
    dead_units = dict()
    __units = dict()
    __BALANCE = 0
    __unit_symbols = ['A', 'B', 'C']

    def __init__(self, balance):
        self.__BALANCE = balance

    def __getitem__(self, item):
        if (item =='balance'):
            return self.__BALANCE
        if (item == 'dict_units'):
            return self.__units
        if (item == 'dead'):
            return self.dead_units

    def get_units(self):
        return list(self.__units.values())

    def random_units(self):

        random_units = random.sample([Swordsman, Archer, Horseman], 3)
        for symbol, unit in zip(self.__unit_symbols, random_units):

            self.add_units(symbol, unit)

    def display_stats(self, unit):
        for symbol, unit_value in self.__units.items():
            if unit_value == unit:
                symbol_for_unit = symbol
                break
        print('----------------')
        print(f"Name: {unit['Name']}\nHP: {unit['HP']}\nSymbol: {symbol_for_unit}\nAvailable move points: {unit['Move_points']}\nDefPts: {unit['def']}\nRange: {unit['range']}\nAttackPoints: {unit['Attack_points']}")
        print('----------------')
        return '\n'
    def add_units(self, symbol, unit):
        self.__units[symbol] = unit

    def display_units(self):
        for unit in self.__units.values():
            self.display_stats(unit)

    def find_nearest_enemy(self, Player):
        nearest_enemy_coords = {}
        for unit in self.get_units():
            min_distance = 10000000000000000
            nearest_enemy = None
            for index, enemy_unit in Player['units'].items():
                square_distance = (abs(unit.Position_i - enemy_unit.Position_i)) ** 2 + (
                    abs(unit.Position_j - enemy_unit.Position_j)) ** 2
                distance = square_distance ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_enemy = enemy_unit
            nearest_enemy_coords[unit] = (nearest_enemy.Position_i, nearest_enemy.Position_j)
        return nearest_enemy_coords

    def move_towards_enemy(self, player, field):
        nearest_enemy_coords = self.find_nearest_enemy(player)
        minDist = 1000000
        foundKey = list(nearest_enemy_coords.keys())[0]
        enemy_pos = [-1,-1]
        for key in nearest_enemy_coords.keys():
            distance = abs((key.Position_i - nearest_enemy_coords[key][0])) ** 2 + abs((key.Position_j - nearest_enemy_coords[key][1])) ** 2
            if distance < minDist:
                enemy_pos[0] = nearest_enemy_coords[key][0]
                enemy_pos[1] = nearest_enemy_coords[key][1]
                foundKey = key
                minDist = distance
        foundKey.prev_positionI = foundKey.Position_i
        foundKey.prev_positionJ = foundKey.Position_j

        for index, defender in player['units'].items():
            defender_pos = [defender.Position_i, defender.Position_j]
            if (defender_pos == enemy_pos):
                target_unit = defender

        if (minDist ** 0.5) <= foundKey['range']:
            target_unit.get_damage(foundKey, field, player)
        else:
            foundKey.Position_i -= 1

        foundKey.save_coordinates()


    def get_damage(self, attacker, defender, field):
        print(f'Bots unit {defender['Name']} was attacked by {attacker['Name']}')
        damage_points = attacker['Attack_points']

        if (defender['def'] != 0):
            while defender['def'] != 0 and damage_points != 0:
                damage_points -= 1
                defender._Unit__def_Points -= 1

        if (defender.HP != 0 and damage_points != 0):
            while defender.HP != 0 and damage_points != 0:
                damage_points -= 1
                defender.HP -= 1
                if (defender.HP == 0):
                    self.die(field, defender)

    def die(self, field, defender):
        print(f'Unit {defender["Name"]} has died!')
        for key, value in self['dict_units'].items():
            if value == defender:
                del self['dict_units'][key]
                break
        field.game_field[defender.Position_i][defender.Position_j] = field.sub_game_field[defender.Position_i][defender.Position_j]


