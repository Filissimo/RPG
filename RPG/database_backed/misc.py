from RPG.database_backed.mongo_operator import Operator


website_updates = Operator('website', 'website')


def define_combat_members():
    player_col = website_updates.get_stat('player_col')
    npc_col = website_updates.get_stat('npc_col')
    player_name = website_updates.get_stat('player_name')
    npc_name = website_updates.get_stat('npc_name')
    return {'player_col': player_col, 'npc_col': npc_col,
            'player_name': player_name, 'npc_name': npc_name}
