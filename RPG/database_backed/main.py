from RPG.database_backed.mongo_tools import EnemiesDB

enemies_db = EnemiesDB()

# Only create a new enemy if the database is empty
if enemies_db.get_all_enemies() is None:
    print('Enemy not found. Creating.')
    enemies_db.create_enemy(enemy_hp=100, enemy_max_hp=100)

print("Changing enemy HP...")
enemies_db.update_enemy_stat('hp', 50)

print('Stats with new stat:')
enemies_db.update_enemy_stat('example_new_stat', 90)
enemies_db.get_all_enemies(print_required=True)

print('Stats with no new stat:')
enemies_db.remove_enemy_stat('example_new_stat')
enemies_db.get_all_enemies(print_required=True)
enemies_db.delete_all_enemies()