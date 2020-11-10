import configparser


def restart():
    player = configparser.ConfigParser()
    enemy = configparser.ConfigParser()
    player['status'] = {
        'in_combat': True,
        'combat_result': 'started'
    }
    player['stats'] = {
        'max_hp': '100',
        'max_mana': '40',
        'mana_regen': '2',
        'physical_dmg': '5',
        'heal': '10',
        'armor': '0',
        'stun': '0'
    }
    player['current'] = {
        'current_hp': '100',
        'current_mana': '40'
    }
    player['max_exp'] = {
        'mini_lvl': '10',
        'max_hp': '70',
        'max_mana': '50',
        'mana_regen': '240',
        'physical_dmg': '100',
        'heal': '240',
        'armor': '100',
        'stun': '120'
    }
    player['exp'] = {
        'lvl_down_counter': 0,
        'mini_lvl': '0',
        'max_hp': '0',
        'max_mana': '0',
        'mana_regen': '0',
        'physical_dmg': '0',
        'heal': '0',
        'armor': '0',
        'stun': '0'
    }
    player['lvl'] = {
        'player_lvl': '0',
        'max_hp': '0',
        'max_mana': '0',
        'mana_regen': '0',
        'physical_dmg': '0',
        'heal': '0',
        'armor': '0',
        'stun': '0'
    }
    enemy['stats'] = {
        'lvl': '0',
        'max_hp': '20',
        'max_mana': '20',
        'physical_dmg': '5'
    }
    enemy['current'] = {
        'current_hp': '20',
        'current_mana': '20'
    }
    enemy['console'] = {
        'message1': 'empty',
        'message2': 'empty'
    }
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)
    with open('enemy.ini', 'w') as configfile:
        enemy.write(configfile)


# restart()
