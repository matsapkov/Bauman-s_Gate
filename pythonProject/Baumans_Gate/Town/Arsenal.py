from Baumans_Gate.Town.GenericBuilding import GenericBuilding


class Arsenal(GenericBuilding):
    def __init__(self):
        super().__init__('Arsenal', 2, 1)

    def buying(self, player):
        super().buying(player)

    def upgrade_armor(self, player):
        if self.amount > 0:
            for unit in player['units'].values():
                unit.DEF += 1
            print('Броня всех ваших юнитов увеличена на 1!')
        else:
            print('У вас нет арсенала для улучшения брони.')