from flask import Flask, render_template, request
from RPG.database_backed.calculator import Calculator
from RPG.database_backed.combat_manager import decision_parser, npc_a_i
from RPG.database_backed.mongo_operator import Operator
from RPG.database_backed.misc import define_combat_members


def game():
    player_name = define_combat_members()['player_name']
    npc_name = define_combat_members()['npc_name']
    player_col = define_combat_members()['player_col']
    npc_col = define_combat_members()['npc_col']
    player_updates = Operator(player_col, player_name)
    npc_updates = Operator(npc_col, npc_name)
    website_updates = Operator('website', 'website')
    need_new_messages = website_updates.get_stat('need_new_messages')
    if need_new_messages is True:
        define_combat_members()
        website_updates.set_stat(player_name, 'New game')
        website_updates.set_stat(npc_name, 'Get ready!')
        website_updates.set_stat('need_new_messages', False)
    npc_decision = npc_a_i()
    calculator = Calculator()

    app = Flask(__name__, template_folder='.')

    @app.route("/")
    def initial_page():
        return show_combat_page()

    @app.route("/attack", methods=['GET', 'POST'])
    def attack():
        if request.method == "POST":
            decision_parser('attack', npc_decision)
            in_combat = website_updates.get_stat('in_combat')
            if in_combat:
                return show_combat_page()
            else:
                return show_out_of_combat_page()

    @app.route("/stun", methods=['GET', 'POST'])
    def stun():
        if request.method == "POST":
            decision_parser('stun', npc_decision)
            in_combat = website_updates.get_stat('in_combat')
            if in_combat:
                return show_combat_page()
            else:
                return show_out_of_combat_page()

    @app.route("/heal", methods=['GET', 'POST'])
    def heal():
        if request.method == "POST":
            decision_parser('heal', npc_decision)
            in_combat = website_updates.get_stat('in_combat')
            if in_combat:
                return show_combat_page()
            else:
                return show_out_of_combat_page()

    @app.route("/poison", methods=['GET', 'POST'])
    def poison():
        if request.method == "POST":
            decision_parser('poison', npc_decision)
            in_combat = website_updates.get_stat('in_combat')
            if in_combat:
                return show_combat_page()
            else:
                return show_out_of_combat_page()

    @app.route("/rejuvenation", methods=['GET', 'POST'])
    def rejuvenation():
        if request.method == "POST":
            decision_parser('rejuvenation', npc_decision)
            in_combat = website_updates.get_stat('in_combat')
            if in_combat:
                return show_combat_page()
            else:
                return show_out_of_combat_page()

    @app.route("/next_combat_same_enemy", methods=['GET', 'POST'])
    def next_combat_same_enemy():
        if request.method == "POST":
            website_updates.set_stat(player_name, 'New fight')
            website_updates.set_stat(npc_name, 'Will be easier))')
            website_updates.set_stat('in_combat', True)
            calculator.new_combat()
            return show_combat_page()

    @app.route("/next_combat_enemy_lvl_up", methods=['GET', 'POST'])
    def next_combat_enemy_lvl_up():
        if request.method == "POST":
            website_updates.set_stat(player_name, 'New fight!')
            website_updates.set_stat(npc_name, 'Get ready for some challenge!')
            calculator.enemy_lvl_up()
            website_updates.set_stat('in_combat', True)
            calculator.new_combat()
            return show_combat_page()

    @app.route("/restart", methods=['GET', 'POST'])
    def restart():
        if request.method == "POST":
            website_updates.reset()
            website_updates.set_stat(player_name, 'New game')
            website_updates.set_stat(npc_name, 'Get ready!')
            define_combat_members()
            return show_combat_page()

    @app.route("/hp_lvl_up", methods=['GET', 'POST'])
    def hp_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('hp')
            return show_out_of_combat_page()

    @app.route("/mana_lvl_up", methods=['GET', 'POST'])
    def mana_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('mana')
            return show_out_of_combat_page()

    @app.route("/mana_regen_lvl_up", methods=['GET', 'POST'])
    def mana_regen_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('mana_regen')
            return show_out_of_combat_page()

    @app.route("/dmg_lvl_up", methods=['GET', 'POST'])
    def dmg_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('dmg')
            return show_out_of_combat_page()

    @app.route("/heal_lvl_up", methods=['GET', 'POST'])
    def heal_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('heal')
            return show_out_of_combat_page()

    @app.route("/armor_lvl_up", methods=['GET', 'POST'])
    def armor_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('armor')
            return show_out_of_combat_page()

    @app.route("/stun_lvl_up", methods=['GET', 'POST'])
    def stun_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('stun')
            return show_out_of_combat_page()

    @app.route("/poison_lvl_up", methods=['GET', 'POST'])
    def poison_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('poison')
            return show_out_of_combat_page()

    @app.route("/rejuvenation_lvl_up", methods=['GET', 'POST'])
    def rejuvenation_lvl_up():
        if request.method == "POST":
            calculator.lvl_up('rejuvenation')
            return show_out_of_combat_page()

    def show_combat_page():
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
        player_current_mana_percent = player_current_mana / player_max_mana * 100
        npc_current_mana_percent = npc_current_mana / npc_max_mana * 100
        index_mana_regen = f"Mana regeneration: {player_updates.get_stat('mana_regen_lvl')}"
        index_physical_dmg = f"Physical damage: {player_updates.get_stat('dmg_lvl')}"
        index_heal = f"Heal: {player_updates.get_stat('heal_lvl')}"
        index_armor = f"Armor: {player_updates.get_stat('armor_lvl')}"
        index_stun = f"Stun: {player_updates.get_stat('stun_lvl')}"
        button_stun = f"⚡({player_updates.get_stat('stun_cooldown_current')})"
        player_stunned = player_updates.get_stat('stun_duration_current')
        npc_stunned = npc_updates.get_stat('stun_duration_current')
        index_player_stunned = f'  -'
        index_npc_stunned = f'  -'
        if player_stunned > 0:
            index_player_stunned = f'  ❌({player_stunned})'
        if npc_stunned > 0:
            index_npc_stunned = f'  ❌({npc_stunned})'

        button_poison = f"🐍({player_updates.get_stat('poison_cooldown_current')})"
        index_poison = f"Poison: {player_updates.get_stat('poison_lvl')}"
        player_poisoned = player_updates.get_stat('poison_duration_current')
        npc_poisoned = npc_updates.get_stat('poison_duration_current')
        index_player_poisoned = f'-'
        index_npc_poisoned = f'-'
        if player_poisoned > 0:
            index_player_poisoned = f'🐍({player_poisoned})'
        if npc_poisoned > 0:
            index_npc_poisoned = f'🐍({npc_poisoned})'

        button_rejuvenation = f"💊({player_updates.get_stat('rejuvenation_cooldown_current')})"
        index_rejuvenation = f"Rejuvenation: {player_updates.get_stat('rejuvenation_lvl')}"
        player_rejuvenating = player_updates.get_stat('rejuvenation_duration_current')
        npc_rejuvenating = npc_updates.get_stat('rejuvenation_duration_current')
        index_player_rejuvenating = f'-'
        index_npc_rejuvenating = f'-'
        if player_rejuvenating > 0:
            index_player_rejuvenating = f'💊({player_rejuvenating})'
        if npc_rejuvenating > 0:
            index_npc_rejuvenating = f'💊({npc_rejuvenating})'

        player_mini_lvl = player_updates.get_stat('mini_lvl')
        player_mini_lvl_max = 5 + player_lvl * 5
        mini_lvl_until_lvl_up = f'Mini lvls to Lvl up: {player_mini_lvl}/{player_mini_lvl_max}'
        availability_of_lvl_up = ''
        if player_mini_lvl_max > player_mini_lvl:
            availability_of_lvl_up = 'Lvl up isn\'t available'
        if player_mini_lvl_max <= player_mini_lvl:
            availability_of_lvl_up = 'YOU CAN LVL UP!!!'
        combat_number = player_updates.get_stat('combat_number')
        won = player_updates.get_stat('won')
        win_ratio = 0
        if won > 0:
            win_ratio = int(won / (combat_number - 1) * 100)
        lost = player_updates.get_stat('lost')
        loss_ratio = 0
        if lost > 0:
            loss_ratio = int(lost / (combat_number - 1) * 100)
        win_loss_info = f'Won: {won} ({win_ratio}%), ' \
                        f'lost: {lost} ({loss_ratio}%), ' \
                        f'This is combat №{combat_number}'
        npc_dmg = npc_updates.get_stat('dmg_lvl')
        npc_armor = npc_updates.get_stat('armor_lvl')
        return render_template("combat_page.html",
                               player_name=player_name,
                               npc_name=npc_name,
                               npc_dmg=npc_dmg,
                               npc_armor=npc_armor,
                               player_hp=player_hp,
                               npc_hp=npc_hp,
                               player_mana=player_mana,
                               npc_mana=npc_mana,
                               message_player=message_player,
                               message_npc=message_npc,
                               player_hp_number=player_current_hp_percent,
                               npc_hp_number=npc_current_hp_percent,
                               player_mana_number=player_current_mana_percent,
                               npc_mana_number=npc_current_mana_percent,
                               index_mana_regen=index_mana_regen,
                               index_physical_dmg=index_physical_dmg,
                               index_heal=index_heal,
                               index_armor=index_armor,
                               index_stun=index_stun,
                               index_rejuvenation=index_rejuvenation,
                               index_poison=index_poison,
                               mini_lvl_until_lvl_up=mini_lvl_until_lvl_up,
                               availability_of_lvl_up=availability_of_lvl_up,
                               win_loss_ratio=win_loss_info,
                               index_player_stunned=index_player_stunned,
                               index_npc_stunned=index_npc_stunned,
                               button_stun=button_stun,
                               index_player_poisoned=index_player_poisoned,
                               index_npc_poisoned=index_npc_poisoned,
                               button_poison=button_poison,
                               index_player_rejuvenating=index_player_rejuvenating,
                               index_npc_rejuvenating=index_npc_rejuvenating,
                               button_rejuvenation=button_rejuvenation
                               )

    def show_out_of_combat_page():
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
        player_current_mana_percent = player_current_mana / player_max_mana * 100
        npc_current_mana_percent = npc_current_mana / npc_max_mana * 100
        index_mana_regen = f"Mana regeneration: {player_updates.get_stat('mana_regen_lvl')}"
        index_physical_dmg = f"Physical damage: {player_updates.get_stat('dmg_lvl')}"
        index_heal = f"Heal: {player_updates.get_stat('heal_lvl')}"
        index_armor = f"Armor: {player_updates.get_stat('armor_lvl')}"
        index_stun = f"Stun: {player_updates.get_stat('stun_lvl')}"
        index_poison = f"Poison: {player_updates.get_stat('poison_lvl')}"
        index_rejuvenation = f"Rejuvenation: {player_updates.get_stat('rejuvenation_lvl')}"
        player_mini_lvl = player_updates.get_stat('mini_lvl')
        player_mini_lvl_max = 5 + player_lvl * 5
        mini_lvl_until_lvl_up = f'Mini lvls to Lvl up: {player_mini_lvl}/{player_mini_lvl_max}'
        availability_of_lvl_up = ''
        if player_mini_lvl_max > player_mini_lvl:
            availability_of_lvl_up = 'Lvl up isn\'t available'
        if player_mini_lvl_max <= player_mini_lvl:
            availability_of_lvl_up = 'YOU CAN LVL UP!!!'
        combat_number = player_updates.get_stat('combat_number')
        won = player_updates.get_stat('won')
        win_ratio = 0
        if won > 0:
            win_ratio = int(won / (combat_number - 1) * 100)
        lost = player_updates.get_stat('lost')
        loss_ratio = 0
        if lost > 0:
            loss_ratio = int(lost / (combat_number - 1) * 100)
        win_loss_info = f'Won: {won} ({win_ratio}%), ' \
                        f'lost: {lost} ({loss_ratio}%), ' \
                        f'Next combat will be №{combat_number}'
        return render_template("out_of_combat_page.html",
                               player_hp=player_hp,
                               npc_hp=npc_hp,
                               player_mana=player_mana,
                               npc_mana=npc_mana,
                               message_player=message_player,
                               message_npc=message_npc,
                               player_hp_number=player_current_hp_percent,
                               npc_hp_number=npc_current_hp_percent,
                               player_mana_number=player_current_mana_percent,
                               npc_mana_number=npc_current_mana_percent,
                               index_mana_regen=index_mana_regen,
                               index_physical_dmg=index_physical_dmg,
                               index_heal=index_heal,
                               index_armor=index_armor,
                               index_stun=index_stun,
                               index_rejuvenation=index_rejuvenation,
                               index_poison=index_poison,
                               mini_lvl_until_lvl_up=mini_lvl_until_lvl_up,
                               availability_of_lvl_up=availability_of_lvl_up,
                               win_loss_ratio=win_loss_info,
                               )

    app.run(host='0.0.0.0')
    # app.run(debug=True)
