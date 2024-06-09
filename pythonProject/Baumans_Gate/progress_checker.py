class ProgressChecker:
    def __init__(self):
        pass

    def progress_check(self, town, player):
        for building in town.buildings:
            if building.name == 'Academy':
                pass
            if building.name == 'Arsenal':
                building.upgrade_armor(player)
            if building.name == 'CraftWorkshop':
                pass
            if building.name == 'DoctorsHouse':
                print(
                    'Отлично! Дом лекаря уже был в вашем городе! Выберите характеристику, которую хотите улучшить!\n')
                print('Характеристики, доступные для улучшения: \n')
                print('1. hit_Points (Здоровье)')
                print('2. def_Points (Защита)')
                choice = input(
                    'Ваши юниты получили баф! Введите название ххарактеристики юнита, к которой вы бы хотели получить +1 за покупку дома лекаря! \n')
                valid_choices = ['hit_Points', 'def_Points', 'move_Points', 'attack_Points', 'attack_Range']
                if choice in valid_choices:
                    for unit in player['units'].values():
                        unit.improve_stat(choice)
                    print(f'Все юниты получили +1 к {choice}!')
                else:
                    print('Недопустимая характеристика. Попробуйте снова.')

            if building.name == 'Forge':
                building.attack_upgrade(player)
            if building.name == 'Market':
                pass
            if building.name == 'Tavern':
                level = building.level
                print(f'Поздравляем! У вас есть таверна уровня {level}')
                print(building)
                for unit in player.get_units().values():
                    unit.move_Points += 0.5 * level
                print(f'Все юниты получили {0.5 * level} к очкам перемещения')
