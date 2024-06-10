import pytest
from unittest.mock import patch
from menu import GameMenu

@pytest.fixture(scope='function', autouse=False)
def prepare_game():
    menu = GameMenu()
    menu.start_game()
    return menu

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

