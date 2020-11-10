def input_db():
    chars = {
        'Scrubby': {
            'collection': 'enemies',
            'combat_number': None,
            'lvl': 1,
            'hp': {'lvl': 50, 'current': 50, 'random': 13, 'exp': None},
            'mana': {'lvl': 20, 'current': 20, 'random': 0, 'exp': None},
            'mana_regen': {'lvl': 1, 'random': 0, 'exp': None},
            'dmg': {'lvl': 5, 'random': 4, 'exp': None},
            'armor': {'lvl': 0, 'random': 1, 'exp': None},
            'stun': {'lvl': 0, 'exp': None, 'cooldown_current': 0,
                     'duration_current': 0}
        },
        'Regenerator': {
            'collection': 'enemies',
            'combat_number': None,
            'lvl': 1,
            'hp': {'lvl': 40, 'current': 40, 'random': 11, 'exp': None},
            'mana': {'lvl': 20, 'current': 20, 'random': 5, 'exp': None},
            'mana_regen': {'lvl': 1, 'random': 1, 'exp': None},
            'dmg': {'lvl': 5, 'random': 3, 'exp': None},
            'heal': {'lvl': 10, 'random': 1, 'exp': None},
            'armor': {'lvl': 1, 'random': 1, 'exp': None},
            'stun': {'lvl': 1, 'random': 1, 'exp': None, 'cooldown_current': 0,
                     'duration_current': 0}
        },
        'Filissimo': {
            'collection': 'players',
            'combat_number': 1,
            'lvl': 0,
            'mini_lvl': 0,
            'lvl_down_counter': 0,
            'hp': {'lvl': 100, 'current': 100, 'exp': 0},
            'mana': {'lvl': 40, 'current': 40, 'exp': 0},
            'mana_regen': {'lvl': 3, 'exp': 0},
            'dmg': {'lvl': 5, 'exp': 0},
            'heal': {'lvl': 10, 'exp': 0},
            'armor': {'lvl': 0, 'exp': 0},
            'stun': {'lvl': 0, 'exp': 0, 'cooldown_current': 0,
                     'duration_current': 0},
            'poison': {'lvl': 0, 'exp': 0, 'cooldown_current': 0,
                       'duration_current': 0},
            'rejuvenation': {'lvl': 0, 'exp': 0, 'cooldown_current': 0,
                             'duration_current': 0}
        },
        'website': {'collection': 'website',
                    'need_new_messages': True,
                    'player_col': 'players',
                    'npc_col': 'enemies',
                    'player_name': 'Filissimo',
                    'npc_name': 'Scrubby',
                    'hp': {'max_exp': 25},
                    'mana': {'max_exp': 30},
                    'mana_regen': {'max_exp': 150},
                    'dmg': {'max_exp': 120},
                    'heal': {'max_exp': 170},
                    'armor': {'max_exp': 250},
                    'stun': {'max_exp': 150, "duration": 1, 'cooldown': 3},
                    'poison': {'max_exp': 150, "duration": 5, 'cooldown': 7},
                    'rejuvenation': {'max_exp': 150, "duration": 5, 'cooldown': 7}
                    }
    }
    return chars