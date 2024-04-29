from player import Player
from field import Field
from units import Unit
from bot import Bot

Swordsman = Unit('Swordsman', 50, 8,3, 5,1, 10, 1,1.5,2)
Horseman = Unit('Horseman', 30, 7, 6,5,1,20,1,1.5,2)
Archer = Unit('Archer', 30,8,2,6,5,15,1,1.5,2)

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

        self.field = Field(int(input("Enter the size of the game field: ")))

        while (self.player['balance'] >= 10) and (len(self.player['units']) <= 3):
            self.player.unit_to_buy()
            self.player.buy_units(Swordsman, Archer, Horseman)

        self.bot.random_units()
        self.field.fill_field()
        self.field.spawn_units(self.player)
        self.field.spawn_BOTunits(self.bot)
        self.field.print_field(self.field.game_field)
        self.field.print_coordinates()

    def main_menu(self):
        while True:

            if len(self.player.get_units()) == 0:
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
                #print(selected_unit.Position_i, selected_unit.Position_i)
                selected_unit.moving(self.field)

                self.field.update_field(self.player, self.bot)
                self.field.print_field(self.field.game_field)
                self.field.print_coordinates()
                #for unit in self.player['units']:
                    #print(unit.Position_i, unit.Position_j)

            elif choice == "2":
                unit_index = int(input("Enter the index of the unit you want to attack: "))
                selected_unit = self.player.get_units()[unit_index]
                selected_unit.attacking(self.bot, self.field)
                self.field.print_field(self.field.game_field)
                self.field.print_coordinates()

            elif choice == "3":
                print('----------BOTS TURN----------')
                self.bot.move_towards_enemy(self.player, self.field)
                self.field.update_field(self.player, self.bot)
                self.field.print_field(self.field.game_field)
                self.field.print_coordinates()
            elif choice == "4":
                self.player.display_units(self.player)
            elif choice == "5":
                self.bot.display_units()
            elif choice == "6":
                print("Quitting the game...")
                break
            else:
                print("Invalid choice. Please try again.")































# print("Welcome to the Strategy Game!")
# field_size = int(input("Enter the size of the game field: "))
# field = Field(field_size)
# bot = Bot(1000000)
# player_balance = int(input("Enter your initial balance: "))
# player = Player(player_balance)
#
# player.unit_to_buy()
# player.buy_units(Swordsman, Archer, Horseman)
# bot.random_units()
# field.fill_field()
# field.spawn_units(player)
# field.spawn_BOTunits(bot)
# field.print_field(field.game_field)
# field.print_coordinates()
# player.display_units(player)
# bot.display_units()
# unit_index = int(input("Enter the index of the unit you want to move: "))
#
# selected_unit = player.get_units()[unit_index]
#
# selected_unit.moving(field)
#
#
# field.update_field(player, bot)
#
# field.print_field(field.game_field)
#
# field.print_coordinates()
#
#
#
# bot.move_towards_enemy(player, field)
#
# field.update_field(player, bot)
#
# field.print_field(field.game_field)
#
# field.print_coordinates()
#
# unit_index = int(input("Enter the index of the unit you want to move: "))
#
# selected_unit = player.get_units()[unit_index]
#
# selected_unit.moving(field)
#
# field.update_field(player, bot)
#
# field.print_field(field.game_field)
#
# field.print_coordinates()
# bot.move_towards_enemy(player,field)
# field.update_field(player, bot)
#
# field.print_field(field.game_field)
#
# field.print_coordinates()
# player.display_units(player)
# bot.display_units()
#
# unit_index = int(input("Enter the index of the unit you want to attack: "))
#
# selected_unit = player.get_units()[unit_index]
#
# selected_unit.attacking(bot, field)
# bot.display_units()
# field.print_field(field.game_field)