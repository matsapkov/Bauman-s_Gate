from Baumans_Gate.database.town_database import CityDatabase
import pickle
city_database = CityDatabase()


class Town:
    def __init__(self):
        print('Ваш город создан! ')
        self.buildings = []

    def __str__(self):
        print('Здания в вашем городе: \n')
        if len(self.buildings) != 0 :
            for index, building in enumerate(self.buildings):
                name = building.name
                wood_cost = building.wood_cost
                stone_cost = building.stone_cost
                if hasattr(building, 'level'):
                    level_ = building.level
                else:
                    level_ = 'У этого здания нет уровня'
                amount = building.amount

                print(f'Номер: {index}; Здание: {name}; Цена в дереве: {wood_cost}; Цена в камне: {stone_cost}; Количество: {amount}; Уровень: {level_};')
        else:
            print('В вашем городе еще нет зданий!')

        return ''

    def append(self, building):
        print(f'Здание {building.name} добавлено в Ваш город!')
        self.buildings.append(building)

    def save_town(self):
        with open(r'pickles\pickle.pkl', 'wb') as f:
            pickle.dump(self, f)
        file_path_ = r'pickles\pickle.pkl'
        city_database.insert_into_(file_path_)

    def update_town(self):
        with open(r'pickles\pickle.pkl', 'wb') as f:
            pickle.dump(self, f)
        with open('pickles/pickle.pkl', 'rb') as f:
            DATA = f.read()
        name = input('Введите имя этого города! \n')
        city_database.update_table_(DATA, name)