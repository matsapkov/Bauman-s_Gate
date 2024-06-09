from Baumans_Gate.Town.GenericBuilding import  GenericBuilding


class Forge(GenericBuilding):
    def __init__(self):
        super().__init__('Forge', 3, 2)

    def buying(self, player):
        super().buying(player)

    def attack_upgrade(self, player, increment=1):
        for unit in player['units'].values():
            unit.attack_points += increment
        print(f'Атака всех юнитов увеличена на {increment}!')





