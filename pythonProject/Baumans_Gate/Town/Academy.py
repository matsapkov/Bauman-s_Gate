from Baumans_Gate.project.units import Unit

class Academy:
    def __init__(self):
        self.name = 'Academy'
        self.stone_cost = 1
        self.wood_cost = 1
        self.amount = 0
        self.pending_units = []
        self.researched_units = []

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
            print('Поздравляем! В вашем городе есть академия! Здесь вы можете создавать и изучать новые типы юнитов!')
        else:
            if(self.amount == 1):
                print('Академия уже есть в городе')
            else:
                print('Недостаточно ресурсов для покупки академии')

    def research_unit(self, player, field):
        print('Итак, давайте создадим вашего нового воина!')
        print('На основании характеристик вашего нового воина будет создан указ об исследовании.')
        print('Чтобы указ начал действовать, мы должны оплатить труды наших офицеров в академии.')
        print('Если Вам не хватает денег на оплату, указ будет отложен, и Вы сможете издать его позднее')

        name = input('Введите имя вашего нового воина: \n')
        hp = int(input('Введите количество очков здоровья: \n'))
        dp = int(input('Введите количество очков защиты: \n'))
        mp = int(input('Введите количество очков перемещения: \n'))
        ap = int(input('Введите количество очков атаки: \n'))
        ar = int(input('Введите радиус атаки: \n'))
        TP = int(input('Введите штраф для перемещения по лесу: \n'))
        SP = int(input('Введите штраф для перемещения по болоту: \n'))
        RP = int(input('Введите штраф для перемещения по холмам: \n'))
        SC = input('Введите принадлежность вашего юнита к какому-то супер-классу: on_foot, shooting, cavalry \n')

        research_cost = (
                                (hp * 2) +
                                (dp * 1.5) +
                                (mp * 3) +
                                (ap * 4) +
                                (ar * 2) +
                                (TP * 1) +
                                (SP * 1) +
                                (RP * 1)
                        ) * 1.2

        print(f'Стоимость разработки нового юнита составляет: {research_cost}')
        if player['balance'] >= research_cost:
            confirm = input(f'У вас достаточно средств для разработки данного юнита. Хотите начать? Да/Нет \n')
            if confirm.lower() == 'да':
                player.balance -= research_cost
                new_unit = Unit(name, hp, dp, mp, ap, ar, TP, SP, RP, SC)
                new_unit.spawn_unit_from_academy(player, field)
                player.get_units()[player.unit_count] = new_unit
                player.unit_count += 1
                print(f'Новый юнит {name} создан и добавлен в Вашу армию')
                self.researched_units.append(new_unit)
            else:
                print('Разработка юнита отложена')
                new_unit = Unit(name, hp, dp, mp, ap, ar, TP, SP, RP, SC)
                self.pending_units.append(new_unit)
        else:
            print('Недостаточно средств для разработки юнита. Юнит будет сохранен и вы сможете исследовать его позднее')
            new_unit = Unit(name, hp, dp, mp, ap, ar, TP, SP, RP, SC)
            self.pending_units.append(new_unit)

    def continue_research(self, player, field):
        for idx, unit in enumerate(self.pending_units):
            print(f"{idx + 1}. {unit['Name']} (Стоимость: {unit['Cost']} монет)")

        choice = int(input('Выберите номер юнита для продолжения исследования: \n')) - 1

        if choice < 0 or choice >= len(self.pending_units):
            print('Недопустимый выбор. Попробуйте снова.')
            return

        unit_to_research = self.pending_units[choice]

        if player['balance'] >= unit_to_research['Cost']:
            player.balance -= unit_to_research['Cost']
            new_unit = Unit(
                name=unit_to_research['Name'],
                hp=unit_to_research['HP'],
                dp=unit_to_research['def'],
                mp=unit_to_research['move_points'],
                ap=unit_to_research['attack_points'],
                ar=unit_to_research['range'],
                TP=unit_to_research['tree_penalty'],
                SP=unit_to_research['swamp_penalty'],
                RP=unit_to_research['rock_penalty'],
                SC=unit_to_research['SC']
            )
            new_unit.spawn_unit_from_academy(player, field)
            player.get_units()[player.unit_count] = new_unit
            player.unit_count += 1
            self.pending_units.pop(choice)
            print(f'Новый юнит "{new_unit['Name']}" создан и добавлен в вашу армию.')
        else:
            print('Недостаточно средств для разработки юнита. Попробуйте снова позже.')

