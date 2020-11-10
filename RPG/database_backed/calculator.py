import random
from RPG.database_backed.mongo_operator import Operator
from RPG.database_backed.misc import define_combat_members

player_col = define_combat_members()['player_col']
npc_col = define_combat_members()['npc_col']
player_name = define_combat_members()['player_name']
npc_name = define_combat_members()['npc_name']
player_updates = Operator(player_col, player_name)
npc_updates = Operator(npc_col, npc_name)
website_updates = Operator('website', 'website')


class Calculator:
    def __init__(self):
        pass

    def define_roles(self, actor, target):
        target_role = ''
        actor_role = ''
        if actor == player_name:
            actor_role = player_updates
        if actor == npc_name:
            actor_role = npc_updates
        if target == player_name:
            target_role = player_updates
        if target == npc_name:
            target_role = npc_updates
        return {'actor_role': actor_role, 'target_role': target_role}

    def randomise_attack(self, dmg):
        return random.randint(int(dmg * 0.7), int(dmg * 1.3))

    def randomise_heal(self, heal):
        return random.randint(int(heal * 1.8), int(heal * 2.2))

    def randomise_stun(self, stun):
        return random.randint(stun, stun * 3)

    def begin_turn(self):
        combat_members = {player_updates, npc_updates}
        for combat_member in combat_members:
            stun_duration_current = combat_member.get_stat('stun_duration_current')
            if stun_duration_current > 0:
                stun_duration_current -= 1
                combat_member.set_stat('stun_duration_current', stun_duration_current)

    def end_turn(self):
        combat_members = {player_updates, npc_updates}
        for combat_member in combat_members:
            stun_cooldown_current = combat_member.get_stat('stun_cooldown_current')
            if stun_cooldown_current > 0:
                stun_cooldown_current -= 1
                combat_member.set_stat('stun_cooldown_current', stun_cooldown_current)
            collection = combat_member.get_stat('collection')
            mana_max = combat_member.get_stat('mana_lvl')
            mana_current = combat_member.get_stat('mana_current')
            mana_regen = combat_member.get_stat('mana_regen_lvl')
            mana_regen_exp = combat_member.get_stat('mana_regen_exp')
            hp_current = combat_member.get_stat('hp_current')
            if mana_regen_exp is not None:
                if mana_max >= mana_current + mana_regen:
                    mana_current = mana_current + mana_regen
                    mana_regen_exp = mana_regen_exp + mana_regen
                else:
                    mana_regen_exp = mana_regen_exp + mana_max - mana_current
                    mana_current = mana_max
                combat_member.set_stat('mana_current', mana_current)
                combat_member.set_stat('mana_regen_exp', mana_regen_exp)
            if hp_current <= 0:
                if collection == npc_col:
                    self.enemy_lvl_up()
                self.new_combat()

    def new_combat(self):
        self.mini_lvl_ups()
        combat_members = {player_updates, npc_updates}
        for combat_member in combat_members:
            hp_max = combat_member.get_stat('hp_lvl')
            mana_max = combat_member.get_stat('mana_lvl')
            combat_member.set_stat('hp_current', hp_max)
            combat_member.set_stat('mana_current', mana_max)
            stun_duration_current = combat_member.get_stat('stun_duration_current')
            stun_cooldown_current = combat_member.get_stat('stun_cooldown_current')
            if stun_duration_current > 0:
                combat_member.set_stat('stun_duration_current', 0)
            if stun_cooldown_current > 0:
                combat_member.set_stat('stun_cooldown_current', 0)
        combat_number = player_updates.get_stat('combat_number')
        combat_number += 1
        player_updates.set_stat('combat_number', combat_number)

    def mini_lvl_ups(self):
        stat_type = ''
        stats_to_lvl_up = ['hp', 'mana', 'mana_regen', 'dmg', 'heal', 'armor', 'stun']
        for stat_type in stats_to_lvl_up:
            lvl_of_stat = player_updates.get_stat(f'{stat_type}_lvl')
            exp_of_stat = player_updates.get_stat(f'{stat_type}_exp')
            mini_lvl_counter = player_updates.get_stat('mini_lvl')
            max_exp_of_stat = website_updates.get_stat(f'{stat_type}_max_exp')
            while exp_of_stat >= max_exp_of_stat:
                exp_of_stat -= max_exp_of_stat
                lvl_of_stat += 1
                mini_lvl_counter += 1
            player_updates.set_stat(f'{stat_type}_lvl', lvl_of_stat)
            player_updates.set_stat(f'{stat_type}_exp', exp_of_stat)
            player_updates.set_stat('mini_lvl', mini_lvl_counter)
        return stat_type

    def lvl_up(self, stat_to_lvl_up):
        lvl = player_updates.get_stat('lvl')
        mini_lvl = player_updates.get_stat('mini_lvl')
        mini_lvl_max = 5 + lvl * 5
        if mini_lvl >= mini_lvl_max:
            lvl += 1
            mini_lvl_after_lvl_up = mini_lvl - lvl * 5
            player_updates.set_stat('mini_lvl', mini_lvl_after_lvl_up)
            player_updates.set_stat('lvl', lvl)
            all_stats = ['hp', 'mana', 'mana_regen', 'dmg', 'heal', 'armor', 'stun']
            for stat_to_change in all_stats:
                if stat_to_change is not stat_to_lvl_up:
                    lvl_of_stat = player_updates.get_stat(f'{stat_to_change}_lvl')
                    max_exp_of_stat = website_updates.get_stat(f'{stat_to_change}_max_exp')
                    lvl_down_counter = player_updates.get_stat('lvl_down_counter')
                    if lvl_of_stat > 0:
                        lvl_of_stat -= 1
                        lvl_down_counter += max_exp_of_stat
                    player_updates.set_stat(f'{stat_to_change}_lvl', lvl_of_stat)
                    player_updates.set_stat('lvl_down_counter', lvl_down_counter)
                elif stat_to_change == stat_to_lvl_up:
                    lvl_down_counter = player_updates.get_stat('lvl_down_counter')
                    exp_of_stat_to_lvl_up = player_updates.get_stat(f'{stat_to_change}_lvl')
                    total_exp_for_lvl_up = lvl * 10 + lvl_down_counter
                    exp_of_stat_to_lvl_up += total_exp_for_lvl_up
                    player_updates.set_stat(f'{stat_to_change}_exp', exp_of_stat_to_lvl_up)
                    player_updates.set_stat('lvl_down_counter', 0)
            lvl_of_stat = player_updates.get_stat(f'{stat_to_lvl_up}_lvl')
            exp_of_stat = player_updates.get_stat(f'{stat_to_lvl_up}_exp')
            max_exp_of_stat = website_updates.get_stat(f'{stat_to_lvl_up}_max_exp')
            while exp_of_stat >= max_exp_of_stat:
                exp_of_stat -= max_exp_of_stat
                lvl_of_stat += 1
            player_updates.set_stat(f'{stat_to_lvl_up}_lvl', lvl_of_stat)
            player_updates.set_stat(f'{stat_to_lvl_up}_exp', exp_of_stat)

            hp_max = player_updates.get_stat('hp_lvl')
            hp_current = player_updates.get_stat('hp_current')
            mana_max = player_updates.get_stat('mana_lvl')
            mana_current = player_updates.get_stat('mana_current')
            if mana_max < mana_current:
                player_updates.set_stat('mana_current', mana_max)
            if hp_max < hp_current:
                player_updates.set_stat('hp_current', hp_max)
        return stat_to_lvl_up

    def enemy_lvl_up(self):
        lvl = npc_updates.get_stat('lvl')
        hp = npc_updates.get_stat('hp_lvl')
        hp_random = npc_updates.get_stat('hp_random')
        dmg = npc_updates.get_stat('dmg_lvl')
        dmg_random = npc_updates.get_stat('dmg_random')
        lvl += 1
        dmg_lvl_up = random.randint(0, dmg_random)
        hp_lvl_up = hp_random - dmg_lvl_up + lvl
        dmg_after_lvl_up = dmg + dmg_lvl_up
        hp_after_lvl_up = hp + hp_lvl_up
        npc_updates.set_stat('lvl', lvl)
        npc_updates.set_stat('hp_lvl', hp_after_lvl_up)
        npc_updates.set_stat('dmg_lvl', dmg_after_lvl_up)
