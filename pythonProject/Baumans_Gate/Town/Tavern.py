class Tavern:
    def __init__(self):
        self.name = 'Tavern'
        self.stone_cost = 1
        self.wood_cost = 1
        self.amount = 0
        self.level = 0
        self.stone_upgrade_cost = 1
        self.wood_upgrade_cost = 1

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return True
        else:
            return False

    def buying(self, player):
        if player.wood >= self.wood_cost and player.stone >= self.stone_cost and self.amount < 1:
            print('Поздравляем! Таверна куплена! Теперь у вас есть таверна 1-го уровня')
            player.stone -= self.stone_cost
            player.wood -= self.wood_cost
            self.amount += 1
            self.level += 1
            self.upgrade_moving(player)
        else:
            if(self.amount == 1):
                print('Таверна уже есть в городе')
            else:
                print('Недостаточно ресурсов для покупки таверны')

    def upgrade(self, player):
        if player.wood >= self.wood_upgrade_cost and player.stone >= self.stone_upgrade_cost and self.level < 4:
            player.stone -= self.stone_cost
            player.wood -= self.wood_cost
            self.level += 1
            print(f'Поздравляем! Вы улучшили таверну! Теперь у ваша таверна имеет уровень {self.level}')
            self.upgrade_moving(player)
        else:
            if self.level >= 4:
                print('Таверна уже достигла максимального уровня')
            else:
                print('Недостаточно ресурсов для улучшения таверны')

    def upgrade_moving(self, player):
        for unit in player.get_units().values():
            unit.move_Points += 0.5
        print(f'Все юниты получили +0.5 к перемещению за уровень {self.level}!')

