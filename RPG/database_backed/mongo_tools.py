import pymongo


class EnemiesDB:
    """
    This class contains all the information about the enemy.
    Can also update specific stats based on stat name.
    """
    def __init__(self):
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        rpg_db = mongo_client["rpg_database"]
        self.enemies_col = rpg_db["enemies"]

    def create_enemy(self, enemy_hp, enemy_max_hp):
        """
        Create a new enemy in the database
        :param enemy_name: name of the new enemy
        :param enemy_hp: initial HP of the new enemy
        :param enemy_max_hp: max hp of the new enemy
        :return: None
        """
        enemy_details = {
            "name": 'enemy',
            "lvl": 1,
            "hp": enemy_hp,
            "max_hp": enemy_max_hp
        }
        self.enemies_col.insert_one(enemy_details)

    def get_all_enemies(self, print_required=False):
        """
        Goes through the list of existing enemies and prints them, if any exist
        If no enemies exist, return None
        :return: Last enemy in the list or None
        """
        for entry in self.enemies_col.find():
            if print_required:
                print(f'--{entry}')
            return entry
        return None

    def update_enemy_stat(self, stat_type, stat_value):
        """
        Update a specific stat of the enemy with a specific value.
        :param enemy_name: name of the enemy to receive the new stat
        :param stat_type: type of the stat tp update
        :param stat_value: value to assign to the stat
        :return: None
        """
        enemy_update_query = {"name": 'enemy'}
        new_stat_value = {"$set": {stat_type: stat_value}}
        self.enemies_col.update_one(enemy_update_query, new_stat_value)

    def remove_enemy_stat(self, stat_type):
        """
        Removes a specific stat from the enemy.
        :param stat_type: type of the stat tp remove
        :return: None
        """
        enemy_update_query = {"name": 'enemy'}
        new_stat_value = {"$unset": {stat_type: ""}}
        self.enemies_col.update_one(enemy_update_query, new_stat_value)

    def delete_all_enemies(self):
        """
        Removes all enemies from the database. Use with care.
        :return:
        """
        self.enemies_col.delete_many({})
