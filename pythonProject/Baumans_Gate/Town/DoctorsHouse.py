class DoctorsHouse:
    def __init__(self):
        self.name = 'DoctorsHouse'
        self.stone_cost = 1
        self.wood_cost = 1
        self.amount = 0
        self.technologies = [
            AlchemyTechnology('Herbal Remedies', 2, 2, 10),
            AlchemyTechnology('Advanced Potions', 4, 4, 20),
            AlchemyTechnology('Elixirs of Vitality', 6, 6, 30)
        ]

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return True
        else:
            return False

    def buying(self, player):
        if player.wood >= self.wood_cost and player.stone >= self.stone_cost and self.amount < 1:
            self.amount += 1
            print('Отлично! Дом лекаря теперь находится в Вашем городе! Здесь вы можете исследовать новые алхимические элементы, повышая тем самым здоровье своим юнитам\n')
            print('Характеристики, доступные для улучшения: \n')
            print('1. hit_Points (Здоровье)')
            print('2. def_Points (Защита)')
            choice = input('Ваши юниты получили баф! Введите название ххарактеристики юнита, к которой вы бы хотели получить +1 за покупку дома лекаря! \n')
            valid_choices = ['hit_Points', 'def_Points', 'move_Points', 'attack_Points', 'attack_Range']
            if choice in valid_choices:
                for unit in player['units'].values():
                    unit.improve_stat(choice)
                print(f'Все юниты получили +1 к {choice}!')
            else:
                print('Недопустимая характеристика. Попробуйте снова.')
        else:
            if (self.amount == 1):
                print(f'{self.name} уже есть в городе')
            else:
                print('Недостаточно ресурсов для покупки дома лекаря')

    def visiting(self, player):
        print('Вы зашли в дом лекаря! Что вам нужно?\n')
        print('1. Показать технологии\n')
        print('2. Исследовать технологию\n')
        choice = input()
        if choice == '1':
            self.show_technologies()
        elif choice == '2':
            name = input('Введите название технологии, которую вы хотите исследовать\n')
            self.research_technology(player, name)
        else:
            print('invalid choice')

    def show_technologies(self):
        for tech in self.technologies:
            if tech.researched:
                status = 'Исследовано'
            else:
                status = 'Не исследовано'
            print(f'{tech.name}: Камень: {tech.stone_cost}, Дерево: {tech.wood_cost}. Статус - {status}')

    def research_technology(self, player, name):
        for tech in self.technologies:
            if tech.name == name:
                if tech.researched:
                    print('Данная технология уже исследована')
                else:
                    if player.wood >= tech.wood_cost and player.stone >= tech.stone_cost:
                        player.stone -= tech.stone_cost
                        player.wood -= tech.wood_cost
                        tech.researched = True
                        for unit in player.get_units().values():
                            unit.HP += tech.hp_increase
                        print(f'{tech.name} успешно исследовано! Здоровье юнитов увеличено на {tech.hp_increase}')
                    else:
                        print('Недостаточно ресурсов для исследования данной технологии')


class AlchemyTechnology:
    def __init__(self, name, stone_cost, wood_cost, hp_increase):
        self.name = name
        self.stone_cost = stone_cost
        self.wood_cost = wood_cost
        self.hp_increase = hp_increase
        self.researched = False
