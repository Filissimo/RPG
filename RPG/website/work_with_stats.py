import configparser
import random


def end_turn():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    max_mana = int(player['stats']['max_mana'])
    current_mana = int(player['current']['current_mana'])
    mana_regen = int(player['stats']['mana_regen'])
    mana_regen_exp = int(player['exp']['mana_regen'])
    player_current_hp = int(player['current']['current_hp'])
    enemy = configparser.ConfigParser()
    enemy.sections()
    enemy.read('enemy.ini')
    enemy_current_hp = int(enemy['current']['current_hp'])
    if max_mana >= current_mana + mana_regen:
        current_mana = current_mana + mana_regen
        mana_regen_exp = mana_regen_exp + mana_regen
    else:
        mana_regen_exp = mana_regen_exp + max_mana - current_mana
        current_mana = max_mana
    player['current']['current_mana'] = str(current_mana)
    player['exp']['mana_regen'] = str(mana_regen_exp)
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)
    if player_current_hp <= 0:
        mini_lvl_ups()
        new_combat()
    if enemy_current_hp <= 0:
        mini_lvl_ups()
        enemy_lvl_up()
        new_combat()


def mini_lvl_ups():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    stats_to_lvl_up = ['max_hp', 'max_mana', 'mana_regen', 'physical_dmg', 'heal', 'armor']
    for stat_type in stats_to_lvl_up:
        player = one_lvl_up(player, stat_type)
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)


def one_lvl_up(player, stat_type):
    stat_to_lvl = int(player['stats'][stat_type])
    exp_of_stat = int(player['exp'][stat_type])
    mini_lvl_counter = int(player['exp']['mini_lvl'])
    lvl_of_stat = int(player['lvl'][stat_type])
    max_exp_of_stat = int(player['max_exp'][stat_type])
    while exp_of_stat >= max_exp_of_stat:
        exp_of_stat -= max_exp_of_stat
        stat_to_lvl += 1
        lvl_of_stat += 1
        mini_lvl_counter += 1
    player['stats'][stat_type] = str(stat_to_lvl)
    player['exp'][stat_type] = str(exp_of_stat)
    player['exp']['mini_lvl'] = str(mini_lvl_counter)
    player['lvl'][stat_type] = str(lvl_of_stat)
    return player


def enemy_lvl_up():
    enemy = configparser.ConfigParser()
    enemy.sections()
    enemy.read('enemy.ini')
    enemy_lvl = int(enemy['stats']['lvl'])
    enemy_max_hp = int(enemy['stats']['max_hp'])
    enemy_physical_dmg = int(enemy['stats']['physical_dmg'])
    enemy_lvl += 1
    dmg_lvl_up = random.randint(1, 3)
    hp_lvl_up = 8 - dmg_lvl_up
    enemy_physical_dmg = enemy_physical_dmg + dmg_lvl_up
    enemy_max_hp = enemy_max_hp + hp_lvl_up
    enemy['stats']['physical_dmg'] = str(enemy_physical_dmg)
    enemy['stats']['max_hp'] = str(enemy_max_hp)
    enemy['stats']['lvl'] = str(enemy_lvl)
    with open('enemy.ini', 'w') as char_configfile:
        enemy.write(char_configfile)


def new_combat():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    enemy = configparser.ConfigParser()
    enemy.sections()
    enemy.read('enemy.ini')
    player_max_hp = player['stats']['max_hp']
    player_max_mp = player['stats']['max_mana']
    player['current']['current_hp'] = player_max_hp
    player['current']['current_mana'] = player_max_mp
    enemy_max_hp = enemy['stats']['max_hp']
    enemy['current']['current_hp'] = enemy_max_hp
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)
    with open('enemy.ini', 'w') as configfile:
        enemy.write(configfile)


def armor_lvl_up():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    lvl = int(player['lvl']['player_lvl'])
    mini_lvl = int(player['exp']['mini_lvl'])
    max_mini_lvl = int(player['max_exp']['mini_lvl'])
    if mini_lvl >= max_mini_lvl:
        lvl += 1
        mini_lvl = mini_lvl - max_mini_lvl
        max_mini_lvl += 1
        player['exp']['mini_lvl'] = str(mini_lvl)
        player['lvl']['player_lvl'] = str(lvl)
        player['max_exp']['mini_lvl'] = str(max_mini_lvl)
        stats_to_lvl_down = ['max_hp', 'max_mana', 'mana_regen', 'physical_dmg', 'heal']
        for stat_type in stats_to_lvl_down:
            player = one_lvl_down(player, stat_type)
        player = one_certain_lvl_up(player, 'armor')
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)


def max_hp_lvl_up():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    lvl = int(player['lvl']['player_lvl'])
    mini_lvl = int(player['exp']['mini_lvl'])
    max_mini_lvl = int(player['max_exp']['mini_lvl'])
    if mini_lvl >= max_mini_lvl:
        lvl += 1
        mini_lvl = mini_lvl - max_mini_lvl
        max_mini_lvl += 1
        player['exp']['mini_lvl'] = str(mini_lvl)
        player['lvl']['player_lvl'] = str(lvl)
        player['max_exp']['mini_lvl'] = str(max_mini_lvl)
        stats_to_lvl_down = ['armor', 'max_mana', 'mana_regen', 'physical_dmg', 'heal']
        for stat_type in stats_to_lvl_down:
            player = one_lvl_down(player, stat_type)
        player = one_certain_lvl_up(player, 'max_hp')
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)


def max_mana_lvl_up():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    lvl = int(player['lvl']['player_lvl'])
    mini_lvl = int(player['exp']['mini_lvl'])
    max_mini_lvl = int(player['max_exp']['mini_lvl'])
    if mini_lvl >= max_mini_lvl:
        lvl += 1
        mini_lvl = mini_lvl - max_mini_lvl
        max_mini_lvl += 1
        player['exp']['mini_lvl'] = str(mini_lvl)
        player['lvl']['player_lvl'] = str(lvl)
        player['max_exp']['mini_lvl'] = str(max_mini_lvl)
        stats_to_lvl_down = ['max_hp', 'armor', 'mana_regen', 'physical_dmg', 'heal']
        for stat_type in stats_to_lvl_down:
            player = one_lvl_down(player, stat_type)
        player = one_certain_lvl_up(player, 'max_mana')
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)


def mana_regen_lvl_up():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    lvl = int(player['lvl']['player_lvl'])
    mini_lvl = int(player['exp']['mini_lvl'])
    max_mini_lvl = int(player['max_exp']['mini_lvl'])
    if mini_lvl >= max_mini_lvl:
        lvl += 1
        mini_lvl = mini_lvl - max_mini_lvl
        max_mini_lvl += 1
        player['exp']['mini_lvl'] = str(mini_lvl)
        player['lvl']['player_lvl'] = str(lvl)
        player['max_exp']['mini_lvl'] = str(max_mini_lvl)
        stats_to_lvl_down = ['max_hp', 'max_mana', 'armor', 'physical_dmg', 'heal']
        for stat_type in stats_to_lvl_down:
            player = one_lvl_down(player, stat_type)
        player = one_certain_lvl_up(player, 'mana_regen')
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)


def physical_dmg_lvl_up():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    lvl = int(player['lvl']['player_lvl'])
    mini_lvl = int(player['exp']['mini_lvl'])
    max_mini_lvl = int(player['max_exp']['mini_lvl'])
    if mini_lvl >= max_mini_lvl:
        lvl += 1
        mini_lvl = mini_lvl - max_mini_lvl
        max_mini_lvl += 1
        player['exp']['mini_lvl'] = str(mini_lvl)
        player['lvl']['player_lvl'] = str(lvl)
        player['max_exp']['mini_lvl'] = str(max_mini_lvl)
        stats_to_lvl_down = ['max_hp', 'max_mana', 'mana_regen', 'armor', 'heal']
        for stat_type in stats_to_lvl_down:
            player = one_lvl_down(player, stat_type)
        player = one_certain_lvl_up(player, 'physical_dmg')
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)


def heal_lvl_up():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    lvl = int(player['lvl']['player_lvl'])
    mini_lvl = int(player['exp']['mini_lvl'])
    max_mini_lvl = int(player['max_exp']['mini_lvl'])
    if mini_lvl >= max_mini_lvl:
        lvl += 1
        mini_lvl = mini_lvl - max_mini_lvl
        max_mini_lvl += 1
        player['exp']['mini_lvl'] = str(mini_lvl)
        player['lvl']['player_lvl'] = str(lvl)
        player['max_exp']['mini_lvl'] = str(max_mini_lvl)
        stats_to_lvl_down = ['max_hp', 'max_mana', 'mana_regen', 'physical_dmg', 'armor']
        for stat_type in stats_to_lvl_down:
            player = one_lvl_down(player, stat_type)
        player = one_certain_lvl_up(player, 'heal')
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)


def one_lvl_down(player, stat_type):
    stat_to_lvl = int(player['stats'][stat_type])
    lvl_of_stat = int(player['lvl'][stat_type])
    lvl_down_counter = int(player['exp']['lvl_down_counter'])
    if lvl_of_stat > 0:
        stat_to_lvl -= 1
        lvl_of_stat -= 1
        lvl_down_counter += 1
    player['stats'][stat_type] = str(stat_to_lvl)
    player['lvl'][stat_type] = str(lvl_of_stat)
    player['exp']['lvl_down_counter'] = str(lvl_down_counter)
    return player


def one_certain_lvl_up(player, stat_type):
    stat_to_lvl = int(player['stats'][stat_type])
    lvl_down_counter = int(player['exp']['lvl_down_counter'])
    lvl_of_stat = int(player['lvl'][stat_type])
    player['stats'][stat_type] = str(stat_to_lvl + lvl_down_counter)
    player['lvl'][stat_type] = str(lvl_of_stat + lvl_down_counter)
    player['exp']['lvl_down_counter'] = '0'
    return player
