from RPG.database_backed.db_operator import Chars

chars_db = Chars()


def restart():
    chars_db.delete_all()
    scrub = {
        'name': 'scrub',
        'lvl': 1,
        'hp': {'lvl': 30, 'current': 30, 'random': 8, 'exp': None},
        'mana': {'lvl': 20, 'current': 20, 'random': 0, 'exp': None},
        'dmg': {'lvl': 5, 'random': 3, 'exp': None},
        'armor': {'lvl': 0, 'random': 0, 'exp': None}
    }
    chars_db.create_enemy(scrub)
    player = {
        'name': 'player',
        'combat_number': 1,
        'lvl': 0,
        'mini_lvl': 0,
        'lvl_down_counter': 0,
        'hp': {'lvl': 100, 'current': 100, 'max_exp': 45, 'exp': 0},
        'mana': {'lvl': 40, 'current': 40, 'max_exp': 50, 'exp': 0},
        'mana_regen': {'lvl': 3, 'max_exp': 240, 'exp': 0},
        'dmg': {'lvl': 5, 'max_exp': 110, 'exp': 0},
        'heal': {'lvl': 10, 'max_exp': 230, 'exp': 0},
        'armor': {'lvl': 0, 'max_exp': 200, 'exp': 0},
        'stun': {'lvl': 0, 'max_exp': 70, 'exp': 0, 'cooldown': 5, 'duration': 2}
    }
    chars_db.create_player(player)
    website = {'name': 'website',
               'player': 0,
               'scrub': 0}
    chars_db.create_website(website)


restart()

