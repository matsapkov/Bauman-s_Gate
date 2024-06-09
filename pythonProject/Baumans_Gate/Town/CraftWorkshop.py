from Baumans_Gate.Town.GenericBuilding import GenericBuilding


class CraftWorkshop(GenericBuilding):
    def __init__(self):
        super().__init__('CraftWorkshop', 3, 3)
        self.max_amount = 4

    def buying(self, player):
        if player.wood >= self.wood_cost and player.stone >= self.stone_cost and self.amount < self.max_amount:
            self.amount += 1
            print(f'Теперь у вас {self.amount} ремесленных мастерских.')
        else:
            print('У вас уже максимальное количество ремесленных мастерских!')

    def pay_rent(self, player):
        if self.amount > 0:
            income = 10 * self.amount
            player.balance += income
            print(f'Ремесленные мастерские пополнили ваш баланс на {income} монет. Текущий баланс: {player.balance}')
        else:
            print('У вас нет ремесленных мастерских для пополнения баланса.')