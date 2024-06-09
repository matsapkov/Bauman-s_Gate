from Baumans_Gate.Town.GenericBuilding import GenericBuilding


class Market(GenericBuilding):
    def __init__(self):
        super().__init__('Market', 2, 3)

    def buying(self, player):
        super().buying(player)

    def exchange_resources(self, player):

        wood_conversion_rate = 10
        stone_conversion_rate = 20

        print(f'Ваш текущий баланс - {player['balance']}')
        balance_to_wood = int(input('Введите количество денег, которое вы хотите обменять на дерево'))
        balance_to_stone = int(input('Введите количество денег, которое вы хотите обменять на камень'))
        if player['balance'] >= (balance_to_wood + balance_to_stone):
            player['balance'] -= (balance_to_wood + balance_to_stone)
            player.wood += balance_to_wood // wood_conversion_rate
            player.stone += balance_to_stone // stone_conversion_rate
            print(
                f'Вы обменяли {balance_to_wood} баланса на {balance_to_wood // 10} дерева и {balance_to_stone} баланса на {balance_to_stone // 20} камня.')
        else:
            print('Недостаточно баланса для обмена ресурсов.')