from RPG.database_backed.calculator import Calculator
from RPG.database_backed.mongo_operator import Operator

website_updates = Operator('website', 'website')
calculator = Calculator()


def attack(actor, target):
    actor_updates = calculator.define_roles(actor, target)['actor_role']
    target_updates = calculator.define_roles(actor, target)['target_role']
    stun_duration_current = actor_updates.get_stat('stun_duration_current')
    if stun_duration_current == 0:
        hp = target_updates.get_stat('hp_current')
        hp_exp = target_updates.get_stat('hp_exp')
        armor = target_updates.get_stat('armor_lvl')
        armor_exp = target_updates.get_stat('armor_exp')
        dmg = actor_updates.get_stat('dmg_lvl')
        dmg_exp = actor_updates.get_stat('dmg_exp')
        this_attack = calculator.randomise_attack(dmg)
        if this_attack > armor:
            hp_after_attack = hp + armor - this_attack
            target_updates.set_stat('hp_current', hp_after_attack)
            if armor_exp is not None:
                armor_exp_after_attack = armor_exp + armor
                target_updates.set_stat('armor_exp', armor_exp_after_attack)
            if hp_exp is not None:
                hp_exp_after_attack = hp_exp + this_attack - armor
                target_updates.set_stat('hp_exp', hp_exp_after_attack)
            if dmg_exp is not None:
                dmg_exp_after_attack = dmg_exp + this_attack
                actor_updates.set_stat('dmg_exp', dmg_exp_after_attack)
            website_updates.set_stat(actor,
                                     f'{actor} damaged {target} for {this_attack - armor} dmg')
        if this_attack <= armor:
            if armor_exp is not None:
                armor_exp_after_attack = armor_exp + this_attack
                target_updates.set_stat('armor_exp', armor_exp_after_attack)
            website_updates.set_stat(actor,
                                     f'{actor} did no harm to {target} at all')
    else:
        console = f'{actor} can\'t move'
        website_updates.set_stat(actor, console)


def self_healing(actor, target):
    actor_updates = calculator.define_roles(actor, target)['actor_role']
    stun_duration_current = actor_updates.get_stat('stun_duration_current')
    if stun_duration_current == 0:
        heal = actor_updates.get_stat('heal_lvl')
        heal_exp = actor_updates.get_stat('heal_exp')
        hp_current = actor_updates.get_stat('hp_current')
        hp_max = actor_updates.get_stat('hp_lvl')
        mana_current = actor_updates.get_stat('mana_current')
        mana_exp = actor_updates.get_stat('mana_exp')
        this_heal = calculator.randomise_heal(heal)
        if mana_current >= heal:
            if hp_max >= hp_current + this_heal:
                hp_current_after_heal = hp_current + this_heal
                actor_updates.set_stat('hp_current', hp_current_after_heal)
                console = f'{actor} healed himself for {this_heal} HP'
                if heal_exp is not None:
                    heal_exp_after_heal = heal_exp + this_heal
                    actor_updates.set_stat('heal_exp', heal_exp_after_heal)
            else:
                hp_current_after_heal = hp_max
                actor_updates.set_stat('hp_current', hp_current_after_heal)
                console = (
                    f'{actor} overhealed himself by '
                    f'{hp_current + this_heal - hp_max} HP')
                if heal_exp is not None:
                    heal_exp_after_heal = hp_max - hp_current
                    actor_updates.set_stat('heal_exp', heal_exp_after_heal)
            mana_current_after_heal = mana_current - heal
            actor_updates.set_stat('mana_current', mana_current_after_heal)
            if mana_exp is not None:
                mana_exp_after_heal = mana_exp + heal
                actor_updates.set_stat('mana_exp', mana_exp_after_heal)
            website_updates.set_stat(actor, console)
        else:
            attack(actor, target)
            console = website_updates.get_stat(actor)
            console = f'Not enough mana for heal, but - {console}'
            website_updates.set_stat(actor, console)
    else:
        console = f'{actor} can\'t move'
        website_updates.set_stat(actor, console)


def stunning(actor, target):
    actor_updates = calculator.define_roles(actor, target)['actor_role']
    target_updates = calculator.define_roles(actor, target)['target_role']
    stun_duration_current = actor_updates.get_stat('stun_duration_current')
    if stun_duration_current == 0:
        stun = actor_updates.get_stat('stun_lvl')
        mana_current = actor_updates.get_stat('mana_current')
        stun_cooldown_current = actor_updates.get_stat('stun_cooldown_current')
        if mana_current >= stun > 0 and stun_cooldown_current == 0:
            stun_cooldown = website_updates.get_stat('stun_cooldown')
            actor_updates.set_stat('stun_cooldown_current', stun_cooldown)
            stun_exp = actor_updates.get_stat('stun_exp')
            hp_current = target_updates.get_stat('hp_current')
            this_stun = calculator.randomise_stun(stun)
            hp_current_after_stun = hp_current - this_stun
            target_updates.set_stat('hp_current', hp_current_after_stun)
            if stun_exp is not None:
                hp_exp = target_updates.get_stat('hp_exp')
                mana_exp = actor_updates.get_stat('mana_exp')
                stun_exp_after_stun = stun_exp + this_stun
                actor_updates.set_stat('stun_exp', stun_exp_after_stun)
                mana_exp_after_stun = mana_exp + stun
                actor_updates.set_stat('mana_exp', mana_exp_after_stun)
                if hp_exp is not None:
                    hp_exp_after_stun = hp_exp + this_stun
                    target_updates.set_stat('hp_exp', hp_exp_after_stun)
            mana_current_after_stun = mana_current - stun
            actor_updates.set_stat('mana_current', mana_current_after_stun)
            stun_duration = website_updates.get_stat('stun_duration')
            target_updates.set_stat('stun_duration_current', stun_duration)
            console = f'{actor} stunned {target} for {this_stun} HP'
            website_updates.set_stat(actor, console)
        else:
            attack(actor, target)
            console = website_updates.get_stat(actor)
            console = f'Can\'t cast stun, but {console}'
            website_updates.set_stat(actor, console)
    else:
        console = f'{actor} can\'t move'
        website_updates.set_stat(actor, console)


def poisoning(actor, target):
    actor_updates = calculator.define_roles(actor, target)['actor_role']
    target_updates = calculator.define_roles(actor, target)['target_role']
    stun_duration_current = actor_updates.get_stat('stun_duration_current')
    if stun_duration_current == 0:
        poison = actor_updates.get_stat('poison_lvl') * 2
        mana_current = actor_updates.get_stat('mana_current')
        poison_cooldown_current = actor_updates.get_stat('poison_cooldown_current')
        if mana_current >= poison > 0 and poison_cooldown_current == 0:
            poison_cooldown = website_updates.get_stat('poison_cooldown')
            actor_updates.set_stat('poison_cooldown_current', poison_cooldown)
            mana_exp = actor_updates.get_stat('mana_exp')
            if mana_exp is not None:
                mana_exp_after_poison = mana_exp + poison
                actor_updates.set_stat('mana_exp', mana_exp_after_poison)
            mana_current_after_poison = mana_current - poison
            actor_updates.set_stat('mana_current', mana_current_after_poison)
            poison_duration = website_updates.get_stat('poison_duration')
            target_updates.set_stat('poison_duration_current', poison_duration)
            console = f'{actor} poisoned {target}'
            website_updates.set_stat(actor, console)
        else:
            attack(actor, target)
            console = website_updates.get_stat(actor)
            console = f'Can\'t cast poison, but {console}'
            website_updates.set_stat(actor, console)
    else:
        console = f'{actor} can\'t move'
        website_updates.set_stat(actor, console)


def self_rejuvenation(actor, target):
    actor_updates = calculator.define_roles(actor, target)['actor_role']
    stun_duration_current = actor_updates.get_stat('stun_duration_current')
    if stun_duration_current == 0:
        rejuvenation = actor_updates.get_stat('rejuvenation_lvl') * 2
        mana_current = actor_updates.get_stat('mana_current')
        rejuvenation_cooldown_current = actor_updates.get_stat('rejuvenation_cooldown_current')
        if mana_current >= rejuvenation > 0 and rejuvenation_cooldown_current == 0:
            rejuvenation_cooldown = website_updates.get_stat('rejuvenation_cooldown')
            actor_updates.set_stat('rejuvenation_cooldown_current', rejuvenation_cooldown)
            mana_exp = actor_updates.get_stat('mana_exp')
            if mana_exp is not None:
                mana_exp_after_rejuvenation = mana_exp + rejuvenation
                actor_updates.set_stat('mana_exp', mana_exp_after_rejuvenation)
            mana_current_after_rejuvenation = mana_current - rejuvenation
            actor_updates.set_stat('mana_current', mana_current_after_rejuvenation)
            rejuvenation_duration = website_updates.get_stat('rejuvenation_duration')
            actor_updates.set_stat('rejuvenation_duration_current', rejuvenation_duration)
            console = f'{actor} rejuvenating'
            website_updates.set_stat(actor, console)
        else:
            attack(actor, target)
            console = website_updates.get_stat(actor)
            console = f'Can\'t cast rejuvenation, but {console}'
            website_updates.set_stat(actor, console)
    else:
        console = f'{actor} can\'t move'
        website_updates.set_stat(actor, console)
