import pymongo
import RPG.database_backed.input_stats as input_stats


class Operator:
    def __init__(self, collection, char_name):
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.rpg_db = mongo_client["rpg_database"]
        self.enemies_col = self.rpg_db["enemies"]
        self.players_col = self.rpg_db['players']
        self.website_col = self.rpg_db['website']
        self.collection = collection
        self.col = self.rpg_db[collection]
        self.char_name = char_name

    def create_website(self, website_data):
        self.website_col.insert_one(website_data)

    def create_enemy(self, char_type):
        self.enemies_col.insert_one(char_type)

    def create_player(self, char_type):
        self.players_col.insert_one(char_type)

    def delete_all(self):
        self.enemies_col.delete_many({})
        self.players_col.delete_many({})
        self.website_col.delete_many({})

    def reset(self):
        self.delete_all()
        chars = input_stats.input_db()
        for char in chars:
            stat_list = chars[char]
            char_type = {'name': char,
                         'stats': {}}
            for stat in stat_list:
                expected_variables_shallow = {'collection', 'combat_number', 'lvl',
                                              'mini_lvl', 'lvl_down_counter', 'player_col',
                                              'npc_col', 'player_name', 'npc_name',
                                              'player', 'npc', 'need_new_messages', 'in_combat'}
                for expected_variable in expected_variables_shallow:
                    if stat == expected_variable:
                        value = chars[char][stat]
                        char_type['stats'][stat] = value
                expected_variables_deep = {'hp', 'mana', 'mana_regen',
                                           'dmg', 'heal', 'armor', 'stun', 'poison', 'rejuvenation'}
                for expected_variable in expected_variables_deep:
                    if stat == expected_variable:
                        sub_stat_list = chars[char][stat]
                        for sub_stat in sub_stat_list:
                            value = chars[char][stat][sub_stat]
                            variable_name = f'{stat}_{sub_stat}'
                            char_type['stats'][variable_name] = value
            if chars[char]['collection'] == 'enemies':
                self.create_enemy(char_type)
            if chars[char]['collection'] == 'players':
                self.create_player(char_type)
            if chars[char]['collection'] == 'website':
                self.create_website(char_type)

    def get_stat(self, stat):
        return self.col.find({'name': self.char_name})[0]['stats'][stat]

    def set_stat(self, stat, value):
        return self.col.update_one({'name': self.char_name}, {"$set": {f'stats.{stat}': value}})
