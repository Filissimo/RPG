from RPG.database_backed.mongo_operator import Operator


website_updates = Operator('website', 'website')


def define_combat_members():
    player_col = website_updates.get_stat('player_col')
    npc_col = website_updates.get_stat('npc_col')
    player_name = website_updates.get_stat('player_name')
    npc_name = website_updates.get_stat('npc_name')
    Operator(player_col, player_name).set_stat('opponent_col', npc_col)
    Operator(npc_col, npc_name).set_stat('opponent_col', player_col)
    Operator(player_col, player_name).set_stat('opponent_name', npc_name)
    Operator(npc_col, npc_name).set_stat('opponent_name', player_name)
    Operator(player_col, player_name).set_stat('won', 0)
    Operator(player_col, player_name).set_stat('lost', 0)
    return {'player_col': player_col, 'npc_col': npc_col,
            'player_name': player_name, 'npc_name': npc_name}
