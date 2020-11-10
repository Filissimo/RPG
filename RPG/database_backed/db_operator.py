import pymongo


class Chars:
    def __init__(self):
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        rpg_db = mongo_client["rpg_database"]
        self.enemies_col = rpg_db["enemies"]
        self.players_col = rpg_db['players']
        self.website_col = rpg_db['website']

    def create_website(self, website_data):
        self.website_col.insert_one(website_data)

    def create_enemy(self, enemy_type):
        self.enemies_col.insert_one(enemy_type)

    def create_player(self, enemy_details):
        self.players_col.insert_one(enemy_details)

    def delete_all(self):
        self.enemies_col.delete_many({})
        self.players_col.delete_many({})
        self.website_col.delete_many({})


class Updates:
    def __init__(self, character_type):
        self.character_type = character_type
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        rpg_db = mongo_client["rpg_database"]
        if character_type == 'scrub':
            self.col = rpg_db["enemies"]
        if character_type == 'player':
            self.col = rpg_db['players']
        if character_type == 'website':
            self.col = rpg_db['website']

    def get_stat(self, stat, sub_stat):
        if sub_stat is None:
            return self.col.find({'name': self.character_type})[0][stat]
        return self.col.find({'name': self.character_type})[0][stat][sub_stat]

    def set_stat(self, stat, sub_stat, value):
        if sub_stat is None and value is None:
            return self.col.update_one({'name': self.character_type}, {"$set": {stat}})
        if value is None:
            return self.col.update_one({'name': self.character_type}, {"$set": {stat: sub_stat}})
        return self.col.update_one({'name': self.character_type}, {"$set": {f'{stat}.{sub_stat}': value}})
