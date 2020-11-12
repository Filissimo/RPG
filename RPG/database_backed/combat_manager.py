from RPG.database_backed.mongo_operator import Operator
import RPG.database_backed.misc as misc
import RPG.database_backed.actions as actions
from  RPG.database_backed.calculator import  Calculator

player_col = misc.define_combat_members()['player_col']
npc_col = misc.define_combat_members()['npc_col']
player_name = misc.define_combat_members()['player_name']
npc_name = misc.define_combat_members()['npc_name']
player_updates = Operator(player_col, player_name)
npc_updates = Operator(npc_col, npc_name)
calculator = Calculator()


def decision_parser(player_decision, npc_decision):
    calculator.begin_turn()
    if player_decision == 'stun':
        actions.stunning(player_name, npc_name)
    if player_decision == 'poison':
        actions.poisoning(player_name, npc_name)
    if player_decision == 'rejuvenation':
        actions.self_rejuvenation(player_name, npc_name)
    if player_decision == 'attack':
        actions.attack(player_name, npc_name)
    if player_decision == 'heal':
        actions.self_healing(player_name, npc_name)
    if npc_decision == 'attack':
        actions.attack(npc_name, player_name)
    calculator.end_turn()


def npc_a_i():
    decision = 'attack'
    return decision
