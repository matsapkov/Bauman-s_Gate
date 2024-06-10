from Baumans_Gate.project.player import Player
from Baumans_Gate.project.field import Field
from Baumans_Gate.project.units import Unit
from Baumans_Gate.project.bot import Bot
import pickle
from Baumans_Gate.database.map_database import Database
from Baumans_Gate.database.town_database import CityDatabase
from Baumans_Gate.project.DarkWizard import DarkWizard, Alien
from Baumans_Gate.Town.Town import Town
from Baumans_Gate.Town.DoctorsHouse import DoctorsHouse
from Baumans_Gate.Town.Forge import Forge
from Baumans_Gate.Town.Market import Market
from Baumans_Gate.Town.Academy import Academy
from Baumans_Gate.Town.Arsenal import Arsenal
from Baumans_Gate.Town.CraftWorkshop import CraftWorkshop
from Baumans_Gate.Town.Tavern import Tavern
from Baumans_Gate.project.progress_checker import ProgressChecker
pc = ProgressChecker()
city_database = CityDatabase()
database = Database()
forge = Forge()
doctors_house = DoctorsHouse()
# generic_building = GenericBuilding()
market = Market()
academy = Academy()
arsenal = Arsenal()
craft_workshop = CraftWorkshop()
tavern = Tavern()
Swordsman = Unit('Swordsman', 50, 8,3, 5,1, 10, 1,1.5,2,SC='on_foot')
Horseman = Unit('Horseman', 30, 7, 6,200,1,20,1,1.5,2, SC='cavalry')
Archer = Unit('Archer', 30,8,2,6,5,15,1,1.5,2, SC='shooting')

class GameMenu:
    def __init__(self):
        self.field = None
        self.player = None
        self.bot = None
        self.town = None

    def start_game(self):
        print("Welcome to the Strategy Game!")

        player_balance = int(input("Enter your initial balance: "))
        self.player = Player(player_balance)
        self.bot = Bot(1000000)

        print('\nХотите сыграть на случайной карте или выбрать уже из заранее созданных?')
        print('1. Сыграть на случайной карте')
        print('2. Сыграть на заранее созданной')
        choice = input()

        if choice == '1':
            self.field = Field(size=int(input("Enter the size of the game field: ")))
        elif choice == '2':
            database.show_maps()
            search_name = input('Введите имя карты, на которой вы хотите сыграть...\n')
            data = database.return_map(search_name)[0]
            with open(r'pickles/searched_pickle.pkl', 'wb') as f:
                f.write(data)
            with open(r'pickles/searched_pickle.pkl', 'rb') as f:
                pickled_data = pickle.load(f)
                field = Field()
                field.copy_from_pickle(pickled_data)

            print(f'Найдена карта {search_name}')
            self.field = field
            print(self.field.obstacles)
            print(f'Препятствия в кастомной карте {self.field.obstacles}')
        else:
            print('Invalid input')

        self.Wizard = DarkWizard(1,1, self.field)
        self.Wizard.Wizards.append(self.Wizard)
        self.alien = Alien(unit=Unit('name', 1,1,1,1,1,1,1,1,1))

        while (self.player['balance'] >= 10) and (len(self.player['units']) < 3):
            self.player.unit_to_buy()
            self.player.buy_units(Swordsman, Archer, Horseman)

        if choice != '2':
            self.field.fill_field()

        print('Вы хотите создать новый город или сыграть на каком-то предыдущем? \n')
        print('1. Создать новый город')
        print('2. Сыграть на предыдущем городе')

        second_choice = input('Выберите действие... \n')

        if second_choice == '1':
            self.town = Town()
            self.town.save_town()
        else:
            login = input('Введите логин пользователя \n')
            user_password = input('Введите пароль для выбранной учетной записи \n')
            data_ = city_database.return_town(login, user_password)[0]
            with open(r'pickles/searched_pickle.pkl', 'wb') as f:
                f.write(data_)
            with open(r'pickles/searched_pickle.pkl', 'rb') as f:
                pickled_data_ = pickle.load(f)
                print(f'Найден город!')
                self.town = pickled_data_
            pc.progress_check(self.town, self.player)



        self.bot.random_units()
        self.field.spawn_units(self.player)
        self.field.spawn_BOTunits(self.bot)
        self.field.spawn_WIZARD(self.Wizard)
        self.field.print_field(self.field.game_field)
        self.field.create_coordinates()
        self.field.print_coordinates()

        print('Перед началом битвы мы можем посетить наш город! Желаете? \n')
        choice = input()
        if choice.lower() == 'да':
            self.visit_town()

    def visit_town(self):
        print('Выберите действие:  \n')
        print('1. Просмотреть состояние города')
        print('2. Зайти в определенное здание')
        print('3. Купить новое здание')
        print('4. Выйти из города')
        choice = int(input())

        if choice == 1:
            print(self.town)

        if choice == 2:
            print('Выберите здание, которое желаете посетить: \n')
            print('1. Академия')
            print('2. Арсенал')
            print('3. Ремесленная мастерская')
            print('4. Дом лекаря')
            print('5. Кузня')
            print('6. Рынок')
            print('7. Таверна')
            choice_ = int(input('Выберите здание, которое вы бы хотели посетить: \n'))

            if choice_ == 1:
                if academy in self.town.buildings:
                    print('Выберите действие в академии: \n')
                    print('1. Начать исследование')
                    print('2. Продолжить исследование')
                    action = int(input('Выберите действие...\n'))
                    if action == 1:
                        academy.research_unit(self.player, self.field)
                    elif action == 2:
                        academy.continue_research(self.player, self.field)
                    else:
                        print('invalid input')
                else:
                    print('Академии еще нет в вашем городе!')
            if choice_ == 2:
                if arsenal in self.town.buildings:
                    print('Бонусы арсенала уже используются!')
                else:
                    print('Арсенала еще нет в вашем городе')
            if choice_ == 3:
                if craft_workshop in self.town.buildings:
                    print('Бонусы мастерских уже используются!')
                else:
                    print('Ни одной мастерской еще нет в вашем горподе')
            if choice_ == 4:
                if doctors_house in self.town.buildings:
                    print('Выберите действие в лавке доктора!')
                    print('1. Посещение')
                    action = int(input('Выберите действие...\n'))
                    if action == 1:
                        doctors_house.visiting(self.player)
                    else:
                        print('invalid input')
                else:
                    print('Лавки доктора еще нет в вашем городе')
            if choice_ == 5:
                if forge in self.town.buildings:
                    print('Бонусы кузни уже используются!')
                else:
                    print('Кузни еще нет в вашем городе')
            if choice_ == 6:
                if market in self.town.buildings:
                    print('Выберите действие на рынке!')
                    print('1. Обмен денег на ресурсы')
                    action = int(input('Выберите действие...\n'))
                    if action == 1:
                        market.exchange_resources(self.player)
                    else:
                        print('invalid input')
                else:
                    print('Рынка еще нет в вашем городе')
            if choice_ == 7:
                if tavern in self.town.buildings:
                    print('Выберите действие в таверне!')
                    print('1. Улучшение')
                    action = int(input('Выберите действие...\n'))
                    if action == 1:
                        tavern.upgrade(self.player)
                    else:
                        print('invalid input')
                else:
                    print('Таверны еще нет в вашем городе')

        if choice == 3:
            print('Мы можем приобрести в наш город следующие здания: \n')
            print('1. Академия')
            print('2. Арсенал')
            print('3. Ремесленная мастерская')
            print('4. Дом лекаря')
            print('5. Кузня')
            print('6. Рынок')
            print('7. Таверна')
            choice__ = int(input('Выберите здание, которое вы бы хотели приобрести \n'))
            if choice__ == 1:
                academy.buying(self.player)
                self.town.append(academy)
            if choice__ == 2:
                arsenal.buying(self.player)
                self.town.append(arsenal)
                arsenal.upgrade_armor(self.player)
            if choice__ == 3:
                craft_workshop.buying(self.player)
                self.town.append(craft_workshop)
            if choice__ == 4:
                doctors_house.buying(self.player)
                self.town.append(doctors_house)
            if choice__ == 5:
                forge.buying(self.player)
                self.town.append(forge)
                forge.attack_upgrade(self.player)
            if choice__ == 6:
                market.buying(self.player)
                self.town.append(market)
            if choice__ == 7:
                tavern.buying(self.player)
                self.town.append(tavern)

        if choice == 4:
            return

    def main_menu(self):
        while True:
            print(f'----------СЕЙЧАС ИДЕТ ХОД: {self.Wizard.turn - 1}----------')
            craft_workshop.pay_rent(self.player)
            if len(self.player['units']) == 0:
                print('----------BOT WON----------')
                print('Игра окончена! Нужно сохранить город!')
                self.town.update_town()
                return '----------BOT WON----------'
            if len(self.bot['dict_units']) == 0:
                print('----------PLAYER WON----------')
                print('Игра окончена! Нужно сохранить город!')
                self.town.update_town()
                return '----------PLAYER WON----------'
            self.field.update_field(self.player, self.bot, self.Wizard)
            self.field.print_field(self.field.game_field)
            self.field.print_coordinates()
            print("\nMain Menu:")
            print("1. Move player unit")
            print("2. Attack with player unit")
            print("3. End turn")
            print("4. Display Player units")
            print('5. Show Player balance')
            print("6. Display Bot units")
            print('7. Visit Town')
            print("8. Quit")

            choice = input("Enter your choice: ")

            if choice == "1":
                unit_index = int(input("Enter the index of the unit you want to move: "))
                selected_unit = self.player.get_units()[unit_index]
                selected_unit.moving(self.field)

                if self.Wizard.TURN % 4 == 0 and self.Wizard.turn != 0:
                    if len(self.Wizard.Wizards) != 0:
                        self.Wizard.spawnAliens()
                        print('--------------ALIEN WAS SPAWNED--------------')
                self.field.update_field(self.player, self.bot, self.Wizard)
                self.field.print_field(self.field.game_field)
                self.field.print_coordinates()
                self.Wizard.turn += 1

            elif choice == "2":
                unit_index = int(input("Enter the index of the unit you want to attack: "))
                selected_unit = self.player.get_units()[unit_index]
                selected_unit.attacking(self.bot, self.field, self.Wizard)

                if len(self.Wizard.Wizards) == 0:

                    self.Wizard.returning(self.player, self.bot, self.field)


                if self.Wizard.TURN % 4 == 0 and self.Wizard.turn != 0:
                    if len(self.Wizard.Wizards) != 0:
                        self.Wizard.spawnAliens()
                        print('--------------ALIEN WAS SPAWNED--------------')
                self.field.update_field(self.player, self.bot, self.Wizard)
                self.field.print_field(self.field.game_field)
                self.field.print_coordinates()
                self.Wizard.turn += 1

            elif choice == "3":
                print('----------BOTS and WIZARDS TURN----------')
                self.bot.move_towards_enemy(self.player, self.field)
                self.field.update_field(self.player, self.bot, self.Wizard)

                if self.Wizard.TURN % 4 == 0 and self.Wizard.turn != 0:
                    if len(self.Wizard.Wizards) != 0:
                        self.Wizard.spawnAliens()
                        print('--------------ALIEN WAS SPAWNED--------------')
                if len(self.Wizard.Wizards) != 0:
                    self.Wizard.catch(self.player, self.bot)
                    self.Wizard.Moving(self.field)
                    self.Wizard.catch(self.player, self.bot)
                self.field.update_field(self.player, self.bot, self.Wizard)
                self.field.print_field(self.field.game_field)
                self.field.print_coordinates()
                self.Wizard.turn += 1

            elif choice == "4":
                self.player.display_units(self.player)
            elif choice == '5':
                print(f'Ваш баланс составляет - {self.player['balance']} денег')
            elif choice == "6":
                self.bot.display_units()
            elif choice == '7':
                self.visit_town()
            elif choice == "8":
                print("Quitting the game...")
                print('Нужно сохранить город!')
                self.town.update_town()
                break
            else:
                print("Invalid choice. Please try again.")
