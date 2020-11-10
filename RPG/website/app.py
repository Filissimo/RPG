from flask import Flask, render_template, request
import configparser
import RPG.website.main as action
import RPG.website.reset as reset
import RPG.website.work_with_stats as change_stats


app = Flask(__name__, template_folder='.')


@app.route("/")
def initial_page():
    return show_stats()


@app.route("/attack", methods=['GET', 'POST'])
def attack():
    if request.method == "POST":
        action.player_attack()
        action.enemy_attack()
        change_stats.end_turn()
        return show_stats()
    else:
        return render_template("combat_page.html")


@app.route("/heal", methods=['GET', 'POST'])
def heal():
    if request.method == "POST":
        action.enemy_attack()
        action.healing()
        change_stats.end_turn()
        return show_stats()
    else:
        return render_template("combat_page.html")


@app.route("/restart", methods=['GET', 'POST'])
def restart():
    if request.method == "POST":
        reset.restart()
        return show_stats()
    else:
        return render_template("combat_page.html")


@app.route("/armor_lvl_up", methods=['GET', 'POST'])
def armor_lvl_up():
    if request.method == "POST":
        change_stats.armor_lvl_up()
        return show_stats()
    else:
        return render_template("combat_page.html")


@app.route("/max_hp_lvl_up", methods=['GET', 'POST'])
def max_hp_lvl_up():
    if request.method == "POST":
        change_stats.max_hp_lvl_up()
        return show_stats()

    else:
        return render_template("combat_page.html")


@app.route("/max_mana_lvl_up", methods=['GET', 'POST'])
def max_mana_lvl_up():
    if request.method == "POST":
        change_stats.max_mana_lvl_up()
        return show_stats()

    else:
        return render_template("combat_page.html")


@app.route("/mana_regen_lvl_up", methods=['GET', 'POST'])
def mana_regen_lvl_up():
    if request.method == "POST":
        change_stats.mana_regen_lvl_up()
        return show_stats()

    else:
        return render_template("combat_page.html")


@app.route("/physical_dmg_lvl_up", methods=['GET', 'POST'])
def physical_dmg_lvl_up():
    if request.method == "POST":
        change_stats.physical_dmg_lvl_up()
        return show_stats()

    else:
        return render_template("combat_page.html")


@app.route("/heal_lvl_up", methods=['GET', 'POST'])
def heal_lvl_up():
    if request.method == "POST":
        change_stats.heal_lvl_up()
        return show_stats()

    else:
        return render_template("combat_page.html")


def show_stats():
    player = configparser.ConfigParser()
    player.sections()
    player.read('player.ini')
    player_current_hp = player['current']['current_hp']
    player_max_hp = player['stats']['max_hp']
    player_max_mana = int(player['stats']['max_mana'])
    player_current_mana = int(player['current']['current_mana'])
    enemy = configparser.ConfigParser()
    enemy.sections()
    enemy.read('enemy.ini')
    enemy_lvl = enemy['stats']['lvl']
    enemy_current_hp = enemy['current']['current_hp']
    enemy_max_hp = enemy['stats']['max_hp']
    enemy_max_mana = int(enemy['stats']['max_mana'])
    enemy_current_mana = int(enemy['current']['current_mana'])
    player_hp = f'My HP: {player_current_hp} / {player_max_hp}'
    enemy_hp = f'{enemy_lvl} lvl Enemy\'s HP: {enemy_current_hp} / {enemy_max_hp}'
    player_mana = f'My MANA: {player_current_mana} / {player_max_mana}'
    enemy_mana = f'Enemy\'s MANA: {enemy_current_mana} / {enemy_max_mana}'
    message1 = enemy['console']['message1']
    message2 = enemy['console']['message2']
    player_current_hp_percent = int(player_current_hp) / int(player_max_hp) * 100
    enemy_current_hp_percent = int(enemy_current_hp) / int(enemy_max_hp) * 100
    index_mana_regen = f"Mana regeneration: {player['stats']['mana_regen']}"
    index_physical_dmg = f"Physical damage: {player['stats']['physical_dmg']}"
    index_heal = f"Heal: {player['stats']['heal']}"
    index_armor = f"Armor: {player['stats']['armor']}"
    return render_template("combat_page.html",
                           player_hp=player_hp,
                           enemy_hp=enemy_hp,
                           player_mana=player_mana,
                           enemy_mana=enemy_mana,
                           message1=message1,
                           message2=message2,
                           player_hp_number=player_current_hp_percent,
                           enemy_hp_number=enemy_current_hp_percent,
                           index_mana_regen=index_mana_regen,
                           index_physical_dmg=index_physical_dmg,
                           index_heal=index_heal,
                           index_armor=index_armor
                           )


if __name__ == '__main__':
    app.run(debug=True)
