import random
import configparser


def enemy_attack():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    current_hp = int(player['current']['current_hp'])
    max_hp_exp = int(player['exp']['max_hp'])
    armor = int(player['stats']['armor'])
    armor_exp = int(player['exp']['armor'])
    enemy = configparser.ConfigParser()
    enemy.sections()
    enemy.read('enemy.ini')
    physical_dmg = int(enemy['stats']['physical_dmg'])
    this_attack = random.randint(int((physical_dmg * 0.7)), int((physical_dmg * 1.3)))
    if this_attack > armor:
        current_hp = current_hp + armor - this_attack
        armor_exp = armor_exp + armor
        enemy['console']['message2'] = f'Enemy damaged you for {this_attack - armor} dmg'
    if this_attack <= armor:
        armor_exp = armor_exp + this_attack
        enemy['console']['message2'] = f'Enemy did no harm to you at all'
    player['exp']['armor'] = str(armor_exp)
    player['current']['current_hp'] = str(current_hp)
    max_hp_exp = max_hp_exp + this_attack
    player['exp']['max_hp'] = str(max_hp_exp)
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)
    with open('enemy.ini', 'w') as configfile:
        enemy.write(configfile)


def player_attack():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    physical_dmg = int(player['stats']['physical_dmg'])
    physical_dmg_exp = int(player['exp']['physical_dmg'])
    enemy = configparser.ConfigParser()
    enemy.sections()
    enemy.read('enemy.ini')
    current_hp = int(enemy['current']['current_hp'])
    this_attack = random.randint(int((physical_dmg * 0.7)), int((physical_dmg * 1.3)))
    current_hp = current_hp - this_attack
    enemy['current']['current_hp'] = str(current_hp)
    enemy['console']['message1'] = f'You attacked enemy for {this_attack} dmg'
    physical_dmg_exp = physical_dmg_exp + this_attack
    player['exp']['physical_dmg'] = str(physical_dmg_exp)
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)
    with open('enemy.ini', 'w') as configfile:
        enemy.write(configfile)


def healing():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    heal = int(player['stats']['heal'])
    heal_exp = int(player['exp']['heal'])
    current_hp = int(player['current']['current_hp'])
    max_hp = int(player['stats']['max_hp'])
    current_mana = int(player['current']['current_mana'])
    max_mana_exp = int(player['exp']['max_mana'])
    enemy = configparser.ConfigParser()
    enemy.sections()
    enemy.read('enemy.ini')
    message1 = enemy['console']['message1']
    message1_copy = message1
    this_heal = random.randint(int((heal * 1.8)), int((heal * 2.2)))
    if current_mana >= heal:
        if max_hp >= current_hp + this_heal:
            current_hp = current_hp + this_heal
            message1 = f'You healed yourself for {this_heal} HP'
            heal_exp = heal_exp + this_heal
        else:
            current_hp = max_hp
            message1 = (
                f'You overhealed yourself by'
                f'{current_hp + this_heal - max_hp} HP')
            heal_exp = max_hp - current_hp
        current_mana = current_mana - heal
        player['current']['current_mana'] = str(current_mana)
        max_mana_exp = max_mana_exp + heal
        player['exp']['max_mana'] = str(max_mana_exp)
    else:
        print('test')
        player_attack()
        message1 = f'Not enough mana for heal, but - {message1_copy}'
    enemy['console']['message1'] = message1
    player['exp']['heal'] = str(heal_exp)
    player['current']['current_hp'] = str(current_hp)
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)
    with open('enemy.ini', 'w') as configfile:
        enemy.write(configfile)


def stunning():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    stun = int(player['stats']['stun'])
    stun_exp = int(player['exp']['stun'])
    current_mana = int(player['current']['current_mana'])
    max_mana_exp = int(player['exp']['max_mana'])
    enemy = configparser.ConfigParser()
    enemy.sections()
    enemy.read('enemy.ini')
    current_hp = int(enemy['current']['current_hp'])
    message1 = enemy['console']['message1']
    message1_copy = message1
    this_stun = random.randint(int((stun * 0.8)), int((stun * 1.2)))
    if current_mana >= stun:
        current_hp = current_hp - this_stun
        message1 = f'You healed yourself for {this_stun} HP'
        stun_exp = stun_exp + this_stun
        current_mana = current_mana - stun
        player['current']['current_mana'] = str(current_mana)
        max_mana_exp = max_mana_exp + stun
        player['exp']['max_mana'] = str(max_mana_exp)
    else:
        print('test')
        player_attack()
        message1 = f'Not enough mana for heal, but - {message1_copy}'
    enemy['console']['message1'] = message1
    player['exp']['heal'] = str(stun_exp)
    enemy['current']['current_hp'] = str(current_hp)
    with open('player.ini', 'w') as char_configfile:
        player.write(char_configfile)
    with open('enemy.ini', 'w') as configfile:
        enemy.write(configfile)
