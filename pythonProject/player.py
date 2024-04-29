
class Player:
    __BALANCE = 0
    __units = []

    def __init__(self, balance):
        self.__BALANCE = balance

    def __getitem__(self, item):
        if (item == 'units'):
            return self.__units
        if (item == 'balance'):
            return self.__BALANCE

    def unit_to_buy(self):
        self.__unit_type = input("Введите тип юнита для покупки (Swordsman, Horseman, Archer): ")
        return self.__unit_type

    def buy_units(self, Swordsman, Archer, Horseman):
        if (self.__unit_type == Swordsman['Name'] and self.__BALANCE >= Swordsman['Cost']):
            self.__units.append(Swordsman)
            self.__BALANCE -= Swordsman['Cost']
        elif (self.__unit_type == Archer['Name'] and self.__BALANCE >= Archer['Cost']):
            self.__units.append(Archer)
            self.__BALANCE -= Archer['Cost']
        elif (self.__unit_type == Horseman['Name'] and self.__BALANCE >= Horseman['Cost']):
            self.__units.append(Horseman)
            self.__BALANCE -= Horseman['Cost']
        else:
            print("Денег нет, но вы держитесь там, всего хорошего Вам")
            return None


    def get_units(self):
        return self.__units

    def display_units(self, player):
        for unit in self.__units:
            unit.display_stats(player)

