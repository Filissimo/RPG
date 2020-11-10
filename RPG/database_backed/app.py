from flask import Flask, render_template, request
from RPG.database_backed.calculator import Calculator
from RPG.database_backed.combat_manager import decision_parser, npc_a_i
from RPG.database_backed.mongo_operator import Operator
from RPG.database_backed.misc import define_combat_members


def game():
    website_updates = Operator('website', 'website')
    player_col = define_combat_members()['player_col']
    npc_col = define_combat_members()['npc_col']
    player_name = define_combat_members()['player_name']
    npc_name = define_combat_members()['npc_name']
    player_updates = Operator(player_col, player_name)
    npc_updates = Operator(npc_col, npc_name)
    npc_decision = npc_a_i()
    calculator = Calculator()
    need_new_messages = website_updates.get_stat('need_new_messages')
    if need_new_messages is True:
        website_updates.set_stat(player_name, 'New game')
        website_updates.set_stat(npc_name, 'Get ready!')
        website_updates.set_stat('need_new_messages', False)

    app = Flask(__name__, template_folder='.')

    @app.route("/")
    def initial_page():
        return show_stats()

    @app.route("/attack", methods=['GET', 'POST'])
    def attack():
        if request.method == "POST":
            decision_parser('attack', npc_decision)
            return show_stats()
        else:
            return render_template("website.html")

    @app.route("/stun", methods=['GET', 'POST'])
    def stun():
        if request.method == "POST":
            decision_parser('stun', npc_decision)
            return show_stats()
        else:
            return render_template("website.html")

    @app.route("/heal", methods=['GET', 'POST'])
    def heal():
        if request.method == "POST":
            decision_parser('heal', npc_decision)
            return show_stats()
        else:
            return render_template("website.html")

    @app.route("/restart", methods=['GET', 'POST'])
    def restart():
        if request.method == "POST":
            website_updates.reset()
            website_updates.set_stat(player_name, 'New game')
            website_updates.set_stat(npc_name, 'Get ready!')
            return show_stats()
        else:
            return render_template("website.html")

    @app.route("/hp_lvl_up", methods=['GET', 'POST'])
    def hp_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('hp')
            return show_stats()
        else:
            return render_template("website.html")

    @app.route("/mana_lvl_up", methods=['GET', 'POST'])
    def mana_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('mana')
            return show_stats()
        else:
            return render_template("website.html")

    @app.route("/mana_regen_lvl_up", methods=['GET', 'POST'])
    def mana_regen_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('mana_regen')
            return show_stats()
        else:
            return render_template("website.html")

    @app.route("/dmg_lvl_up", methods=['GET', 'POST'])
    def dmg_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('dmg')
            return show_stats()
        else:
            return render_template("website.html")

    @app.route("/heal_lvl_up", methods=['GET', 'POST'])
    def heal_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('heal')
            return show_stats()
        else:
            return render_template("website.html")

    @app.route("/armor_lvl_up", methods=['GET', 'POST'])
    def armor_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('armor')
            return show_stats()
        else:
            return render_template("website.html")

    @app.route("/stun_lvl_up", methods=['GET', 'POST'])
    def stun_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('stun')
            return show_stats()
        else:
            return render_template("website.html")

    def show_stats():
        player_current_hp = player_updates.get_stat('hp_current')
        player_max_hp = player_updates.get_stat('hp_lvl')
        player_max_mana = player_updates.get_stat('mana_lvl')
        player_current_mana = player_updates.get_stat('mana_current')
        npc_lvl = npc_updates.get_stat('lvl')
        npc_current_hp = npc_updates.get_stat('hp_current')
        npc_max_hp = npc_updates.get_stat('hp_lvl')
        npc_max_mana = npc_updates.get_stat('mana_lvl')
        npc_current_mana = npc_updates.get_stat('mana_current')
        player_lvl = player_updates.get_stat('lvl')
        player_hp = f'{player_lvl} lvl {player_name}\'s HP: {player_current_hp} / {player_max_hp}'
        npc_hp = f'{npc_lvl} lvl {npc_name}\'s HP: {npc_current_hp} / {npc_max_hp}'
        player_mana = f'My MANA: {player_current_mana} / {player_max_mana}'
        npc_mana = f'Enemy\'s MANA: {npc_current_mana} / {npc_max_mana}'
        message_player = website_updates.get_stat(player_name)
        message_npc = website_updates.get_stat(npc_name)
        player_current_hp_percent = player_current_hp / player_max_hp * 100
        npc_current_hp_percent = npc_current_hp / npc_max_hp * 100
        index_mana_regen = f"Mana regeneration: {player_updates.get_stat('mana_regen_lvl')}"
        index_physical_dmg = f"Physical damage: {player_updates.get_stat('dmg_lvl')}"
        index_heal = f"Heal: {player_updates.get_stat('heal_lvl')}"
        index_armor = f"Armor: {player_updates.get_stat('armor_lvl')}"
        index_stun = f"Stun: {player_updates.get_stat('stun_lvl')}"
        button_stun = f"⚡({player_updates.get_stat('stun_cooldown_current')})"
        player_stunned = player_updates.get_stat('stun_duration_current')
        npc_stunned = npc_updates.get_stat('stun_duration_current')
        index_player_stunned = f'✨({player_stunned})'
        index_npc_stunned = f'✨({npc_stunned})'
        if player_stunned > 0:
            index_player_stunned = f'❌({npc_stunned})'
        if npc_stunned > 0:
            index_npc_stunned = f'❌({npc_stunned})'
        player_mini_lvl = player_updates.get_stat('mini_lvl')
        player_mini_lvl_max = 5 + player_lvl * 5
        mini_lvl_until_lvl_up = f'Mini lvls to Lvl up: {player_mini_lvl}/{player_mini_lvl_max}'
        availability_of_lvl_up = ''
        if player_mini_lvl_max > player_mini_lvl:
            availability_of_lvl_up = 'Lvl up isn\'t available'
        if player_mini_lvl_max <= player_mini_lvl:
            availability_of_lvl_up = 'YOU CAN LVL UP!!!'
        combat_number = player_updates.get_stat('combat_number')
        win_loss_info = ''
        if combat_number > 1:
            win_loss_ratio = int((npc_lvl - 1) / (combat_number - 1) * 100)
            win_loss_info = f'Won: {npc_lvl - 1} ({win_loss_ratio}%), ' \
                            f'lost: {combat_number - npc_lvl}.   ' \
                            f'This is combat №{combat_number}'
        if combat_number == 1:
            win_loss_info = f'Won: {npc_lvl - 1} (0%),   ' \
                            f'lost: {combat_number - npc_lvl}.   ' \
                            f'This is combat №{combat_number}'
        return render_template("website.html",
                               player_hp=player_hp,
                               npc_hp=npc_hp,
                               player_mana=player_mana,
                               npc_mana=npc_mana,
                               message_player=message_player,
                               message_npc=message_npc,
                               player_hp_number=player_current_hp_percent,
                               npc_hp_number=npc_current_hp_percent,
                               index_mana_regen=index_mana_regen,
                               index_physical_dmg=index_physical_dmg,
                               index_heal=index_heal,
                               index_armor=index_armor,
                               index_stun=index_stun,
                               mini_lvl_until_lvl_up=mini_lvl_until_lvl_up,
                               availability_of_lvl_up=availability_of_lvl_up,
                               win_loss_ratio=win_loss_info,
                               index_player_stunned=index_player_stunned,
                               index_npc_stunned=index_npc_stunned,
                               button_stun=button_stun
                               )

    app.run(host='0.0.0.0')
