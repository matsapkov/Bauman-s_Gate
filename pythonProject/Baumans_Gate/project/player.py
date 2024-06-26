class Player:
    __BALANCE = 0
    __units = dict()
    dead_units = []
    unit_count = 0  # Счетчик для генерации уникальных ключей
    wood = 200
    stone = 200

    def __init__(self, balance):
        self.__BALANCE = balance

    def __getitem__(self, item):
        if item == 'units':
            return self.__units
        if item == 'balance':
            return self.__BALANCE
        if item == 'dead':
            return self.dead_units

    def unit_to_buy(self):
        self.__unit_type = input("Введите тип юнита для покупки (Swordsman, Horseman, Archer): ")
        return self.__unit_type

    def buy_units(self, Swordsman, Archer, Horseman):
        if self.__unit_type == Swordsman['Name'] and self.__BALANCE >= Swordsman['Cost']:
            self.__units[self.unit_count] = Swordsman
            self.__BALANCE -= Swordsman['Cost']
            self.unit_count += 1  # Увеличиваем счетчик
        elif self.__unit_type == Archer['Name'] and self.__BALANCE >= Archer['Cost']:
            self.__units[self.unit_count] = Archer
            self.__BALANCE -= Archer['Cost']
            self.unit_count += 1  # Увеличиваем счетчик
        elif self.__unit_type == Horseman['Name'] and self.__BALANCE >= Horseman['Cost']:
            self.__units[self.unit_count] = Horseman
            self.__BALANCE -= Horseman['Cost']
            self.unit_count += 1  # Увеличиваем счетчик
        else:
            print("Денег нет, но вы держитесь там, всего хорошего Вам")
            return None

    def get_units(self):
        return self.__units

    def display_units(self, player):
        for unit in self.__units.values():
            unit.display_stats(player)

    def check_balance(self):
        print(f'Текущее состояние казны: Дерево - {self.wood}, Камень - {self.stone}')

    @property
    def balance(self):
        return self.__BALANCE

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError("Баланс не может быть отрицательным.")
        self.__BALANCE = value

    @property
    def WOOD(self):
        return self.wood

    @WOOD.setter
    def WOOD(self, value):
        if value < 0:
            raise ValueError("Количество дерева не может быть отрицательным.")
        self.wood = value

    @property
    def STONE(self):
        return self.stone

    @STONE.setter
    def STONE(self, value):
        if value < 0:
            raise ValueError("Количество камня не может быть отрицательным.")
        self.stone = value