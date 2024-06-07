from player import Player
from field import Field
from units import Unit
from bot import Bot
import pickle
from map_creator.create_map import MapCreator
from database.map_database import Database
from DarkWizard import DarkWizard, Alien

database = Database()
Swordsman = Unit('Swordsman', 50, 8,3, 5,1, 10, 1,1.5,2,SC='on_foot')
Horseman = Unit('Horseman', 30, 7, 6,5,1,20,1,1.5,2, SC='cavalry')
Archer = Unit('Archer', 30,8,2,6,5,15,1,1.5,2, SC='shooting')

class GameMenu:
    def __init__(self):
        self.field = None
        self.player = None
        self.bot = None

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
            with open('pickles/searched_pickle.pkl', 'wb') as f:
                f.write(data)
            with open('pickles/searched_pickle.pkl', 'rb') as f:
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

        while (self.player['balance'] >= 10) and (len(self.player['units']) <= 3):
            self.player.unit_to_buy()
            self.player.buy_units(Swordsman, Archer, Horseman)

        if choice == 1:
            self.field.fill_field()

        self.bot.random_units()

        self.field.spawn_units(self.player)
        self.field.spawn_BOTunits(self.bot)

        self.field.spawn_WIZARD(self.Wizard)
        self.field.print_field(self.field.game_field)
        self.field.create_coordinates()
        self.field.print_coordinates()

    def main_menu(self):
        while True:

            print(f'----------СЕЙЧАС ИДЕТ ХОД: {self.Wizard.turn - 1}----------')

            if len(self.player['units']) == 0:
                print('----------BOT WON----------')
                break
            if len(self.bot['dict_units']) == 0:
                print('----------PLAYER WON----------')
                break

            print("\nMain Menu:")
            print("1. Move player unit")
            print("2. Attack with player unit")
            print("3. End turn")
            print("4. Display Player units")
            print("5. Display Bot units")
            print("6. Quit")

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
            elif choice == "5":
                self.bot.display_units()
            elif choice == "6":
                print("Quitting the game...")
                break
            else:
                print("Invalid choice. Please try again.")
