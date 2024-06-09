class GenericBuilding:
    def __init__(self, name, stone_cost, wood_cost):
        self.name = name
        self.stone_cost = stone_cost
        self.wood_cost = wood_cost
        self.amount = 0

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return True
        else:
            return False

    def buying(self, player):
        if player.wood >= self.wood_cost and player.stone >= self.stone_cost and self.amount < 1:
            self.amount += 1
            player.stone -= self.stone_cost
            player.wood -= self.wood_cost
            print(f'Поздравляем! {self.name} куплен(а)!')
        else:
            if (self.amount == 1):
                print(f'{self.name} уже есть в городе')
            else:
                print('Недостаточно ресурсов для покупки таверны')