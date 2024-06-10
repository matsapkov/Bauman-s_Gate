import pytest
import io
import pickle
from unittest.mock import patch
from menu import GameMenu
import time
from Baumans_Gate.database.map_database import Database
database = Database()
@pytest.fixture(scope='function', autouse=False)
def prepare_game():
    menu = GameMenu()
    return menu

#Тест номер 1
def test_bot_wins(prepare_game):
    fake_inputs = [
        20,
        '2',
        'Тест2',
        'Horseman',
        '2',
        'лох',
        'лох',
        'нет',
        'Тест'
    ]

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()
        prepare_game.player.get_units().clear()
        result = prepare_game.main_menu()

    assert result == '----------BOT WON----------'

#Тест номер 2
def test_player_wins(prepare_game):
    fake_inputs = [
        20,
        '2',
        'Тест2',
        'Horseman',
        '2',
        'лох',
        'лох',
        'нет',
        'Тест'
    ]

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()
        prepare_game.bot['dict_units'].clear()
        result = prepare_game.main_menu()

    assert result == '----------PLAYER WON----------'

#Тест номер 3
def test_check_penalty(prepare_game):
    fake_inputs = [
        20,
        '2',
        'Тест2',
        'Horseman',
        '2',
        'лох',
        'лох',
        'нет',
        'Тест'
    ]
    fake_inputs1 = ['F0', 'F5']

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()
        for unit in prepare_game.player['units'].values():
            UNIT = unit
        with patch('builtins.input', side_effect=fake_inputs1):
            UNIT.moving(prepare_game.field)
            prepare_game.field.update_field(prepare_game.player, prepare_game.bot, prepare_game.Wizard)
            prepare_game.field.print_field(prepare_game.field.game_field)
            start_position = (unit.Position_i, unit.Position_j)
            target_cell = (5, 5)
            path, penalty = prepare_game.field.shortest_path_with_penalty(start_position, target_cell, UNIT)
            UNIT.moving(prepare_game.field)
            prepare_game.field.update_field(prepare_game.player, prepare_game.bot, prepare_game.Wizard)
            prepare_game.field.print_field(prepare_game.field.game_field)
        expected_penalty = 5
        print(f'Real path {path} and  penalty {penalty}')
        assert expected_penalty == penalty

#Тесты номер 4 и 5
def test_attack_range(prepare_game):
    fake_inputs = [20, '2', 'Тест2', 'Horseman', '2', 'лох', 'лох', 'нет']
    fake_inputs1 = ['F0', '0']

    #Тест на отсутсвие регистрации атаки и  дальность атаки
    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()
    for unit in prepare_game.player['units'].values():
        UNIT = unit
        with patch('builtins.input', side_effect=fake_inputs1):
            with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
                UNIT.attacking(prepare_game.bot, prepare_game.field, prepare_game.Wizard)
                output = fake_stdout.getvalue()
                assert 'Attack is impossible' in output

        #Тест на проверку регистрации атаки и дальность
        UNIT.RANGE = 2000
        for enemy in prepare_game.bot['dict_units'].values():
            enemy.Position_i = 6
            enemy.Position_j = 6
            break
        fake_inputs2 = ['G6', '0']
        with patch('builtins.input', side_effect=fake_inputs2):
            with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
                UNIT.attacking(prepare_game.bot, prepare_game.field, prepare_game.Wizard)
                output = fake_stdout.getvalue()
                assert f'Bots unit {enemy['Name']} was attacked by {UNIT['Name']}' in output

#Тест номер 6
def test_moving(prepare_game):

    fake_inputs = [20, '2', 'Тест2', 'Horseman', '2', 'лох', 'лох', 'нет']
    fake_inputs1 = ['H6']

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()
    for unit in prepare_game.player['units'].values():
        UNIT = unit
        with patch('builtins.input', side_effect=fake_inputs1):
            with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
                UNIT.moving(prepare_game.field)
                output = fake_stdout.getvalue()
                assert 'Target cell is not accessible.' in output

#Тест номер 7
def test_die(prepare_game):
    fake_inputs = [20, '2', 'Тест2', 'Horseman', '2', 'лох', 'лох', 'нет']

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()

    for unit in prepare_game.player['units'].values():
        UNIT = unit
        break

    with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
        UNIT.die(prepare_game.field, prepare_game.player)
        output = fake_stdout.getvalue()
        assert f'Unit {UNIT["Name"]} has died!' in output

#Тест номер 8
def test_unit_def(prepare_game):
    fake_inputs = [20, '2', 'Тест2', 'Horseman', '2', 'лох', 'лох', 'нет']

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()

    for unit in prepare_game.player['units'].values():
        UNIT = unit
        break

    UNIT.RANGE = 2000
    UNIT.attack_points = 2

    for enemy in prepare_game.bot['dict_units'].values():
        ENEMY = enemy
        break
    expected_def_points = ENEMY['def'] - 2
    prepare_game.bot.get_damage(UNIT, ENEMY, prepare_game.field)

    assert ENEMY['def'] == expected_def_points

#Тест номер 9
def test_buying(prepare_game):

    fake_inputs = [20, '2', 'Тест2', 'Horseman', '2', 'лох', 'лох', 'нет']

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()

    expected_name = 'Horseman'

    for unit in prepare_game.player['units'].values():
        UNIT = unit
        break

    assert UNIT['Name'] == expected_name

#Тест номер 10
def test_bot_actions(prepare_game):

    fake_inputs = [20, '2', 'Тест2', 'Horseman', '2', 'лох', 'лох', 'нет']

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()
    for unit in prepare_game.player['units'].values():
        UNIT = unit
        UNIT.Position_i = 0
        UNIT.Position_j = 6
        prepare_game.field.update_field(prepare_game.player, prepare_game.bot, prepare_game.Wizard)
        break

    for enemy in prepare_game.bot['dict_units'].values():
        if enemy['Name'] != 'Archer':
            ENEMY = enemy
            ENEMY.Position_i = 5
            ENEMY.Position_j = 6
            break

    prepare_game.field.update_field(prepare_game.player, prepare_game.bot, prepare_game.Wizard)
    expected_coords = (ENEMY.Position_i - 1, ENEMY.Position_j)
    prepare_game.bot.move_towards_enemy(prepare_game.player, prepare_game.field)
    prepare_game.field.update_field(prepare_game.player, prepare_game.bot, prepare_game.Wizard)
    prepare_game.field.print_field(prepare_game.field.game_field)

    assert (ENEMY.Position_i, ENEMY.Position_j) == expected_coords

#тест 10.1 на совершение атаки
def test_bot_action_attack(prepare_game):
    fake_inputs = [20, '2', 'Тест2', 'Horseman', '2', 'лох', 'лох', 'нет']

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()

    for unit in prepare_game.player['units'].values():
        UNIT = unit
        break

    for enemy in prepare_game.bot['dict_units'].values():
        if enemy['Name'] == 'Archer':
            enemy.RANGE = 200000000
            enemy.Position_i = 2
            enemy.Position_j = 6
            prepare_game.field.update_field(prepare_game.player, prepare_game.bot, prepare_game.Wizard)
            prepare_game.field.print_field(prepare_game.field.game_field)
            break
    expected_def = UNIT.DEF - 6
    prepare_game.bot.move_towards_enemy(prepare_game.player, prepare_game.field)
    prepare_game.field.update_field(prepare_game.player, prepare_game.bot, prepare_game.Wizard)
    prepare_game.field.print_field(prepare_game.field.game_field)
    assert expected_def == UNIT['def']

#тест 11
def test_field_print(prepare_game):
    fake_inputs = [20, '2', 'Тест2', 'Horseman', '2', 'лох', 'лох', 'нет']

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()

    for unit in prepare_game.player['units'].values():
        assert prepare_game.field.game_field[unit.Position_i][unit.Position_j] == 0

    for unit in prepare_game.bot['dict_units'].values():
        assert prepare_game.field.game_field[unit.Position_i][unit.Position_j] == 'A' or prepare_game.field.game_field[unit.Position_i][unit.Position_j] == 'B' or prepare_game.field.game_field[unit.Position_i][unit.Position_j] == 'C'


#Тест 12. Проверка, что черный маг призывает чужих раз в два хода
def test_extra_task(prepare_game):
    fake_inputs = [20, '2', 'Тест2', 'Horseman', '2', 'лох', 'лох', 'нет']
    fake_inputs1 = ['3', '3', '3', '3', '8', 'Тест']
    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()

    with patch('builtins.input', side_effect=fake_inputs1):
        prepare_game.main_menu()

    assert len(prepare_game.Wizard.Aliens) == 1

#----------------------------------------------------------------------ТЕСТЫ ДЛЯ ЛР-3(4-7)------------------------------------------------------------------------------------
#Тест 16
def test_map_loading(prepare_game):
    data = database.return_map('Тест2')[0]
    with open(r'pickles/searched_pickle.pkl', 'wb') as f:
        f.write(data)
    with open(r'pickles/searched_pickle.pkl', 'rb') as f:
        pickled_data = pickle.load(f)

    assert pickled_data.game_field is not None


#Тест 17
def test_building_upgrade(prepare_game):

    fake_inputs = [2000, '1', '15', 'Horseman', 'Archer', 'Swordsman', '1', 'ТестовоеСозданиеГорода', 'тестики', 'тестики', 'да', '3', '7']

    fake_inputs1 = ['7', '2', '7', '1', '8', 'ТестовоеСозданиеГорода']
    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()

    with patch('builtins.input', side_effect=fake_inputs1):
        prepare_game.main_menu()

    for building in prepare_game.town.buildings:
        if building.name == 'Tavern':
            if building.level == 2:
                assert True
            else:
                assert False
def test_bonuses(prepare_game):
    fake_inputs = [2000, '1', '15', 'Horseman', 'Archer', 'Swordsman', '1', 'ТестовоеСозданиеГорода', 'тестики',
                   'тестики', 'да', '3', '2']
    fake_inputs1 = ['3', '8', 'ТестовоеСозданиеГорода']

    with patch('builtins.input', side_effect=fake_inputs):
        prepare_game.start_game()

    with patch('builtins.input', side_effect=fake_inputs1):
        prepare_game.main_menu()

    actual_def = list()

    for unit in prepare_game.player['units'].values():
        actual_def.append(unit['def'])

    assert actual_def == [8,9,9]

def test_saves(prepare_game):
    # fake_inputs = [2000, '1', '15', 'Horseman', 'Archer', 'Swordsman', '1', 'ТестовоеСозданиеГорода', 'тестики',
    #                'тестики', 'да', '3', '7']
    #
    # fake_inputs1 = ['3', '7', '2', '7','1','8','ТестовоеСозданиеГорода']

    fake_inputs3 = [2000, '1', '15', 'Horseman', 'Archer', 'Swordsman', '2', 'тестики', 'тестики', 'да', '1']

    fake_inputs4 = ['8','ТестовоеСозданиеГорода']

    # with patch('builtins.input', side_effect=fake_inputs):
    #     prepare_game.start_game()
    #
    # time.sleep(3)
    #
    # with patch('builtins.input', side_effect=fake_inputs1):
    #     prepare_game.main_menu()

    time.sleep(3)

    with patch('builtins.input', side_effect=fake_inputs3):
        prepare_game.start_game()

    with patch('builtins.input', side_effect=fake_inputs4):
        prepare_game.main_menu()

    for building in prepare_game.town.buildings:
        if building.name == 'Tavern' and building.level == 2:
            assert True
        else:
            assert False
