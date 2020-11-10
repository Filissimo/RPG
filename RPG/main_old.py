import random


class RPGRunner:
    def __init__(self):
        self.combat = True
        self.max_hp_amount_lvl = 0
        self.max_hp_amount_exp = 0
        self.physical_dmg_lvl = 0
        self.physical_dmg_exp = 0
        self.max_mp_amount_lvl = 0
        self.max_mp_amount_exp = 0
        self.mp_regen_lvl = 0
        self.mp_regen_exp = 0
        self.heal_lvl = 0
        self.heal_exp = 0
        self.stun_lvl = 0
        self.stun_exp = 0
        self.hp_regen_lvl = 0
        self.hp_regen_exp = 0
        self.enemy_lvl = 0

        self.player = {
            'max_hp_amount': 100 + self.max_hp_amount_lvl,
            'physical_dmg': 5 + self.physical_dmg_lvl,
            'max_mp_amount': 20 + self.max_mp_amount_lvl,
            'mp_regen': 1 + self.mp_regen_lvl,
            'heal': 10 + self.hp_regen_lvl
        }
        self.player['current_hp_amount'] = self.player['max_hp_amount']
        self.player['current_mp_amount'] = self.player['max_mp_amount']

        self.enemy = {
            'max_hp_amount': 20 + self.enemy_lvl * 5,
            'current_hp_amount': 20 + self.enemy_lvl * 5,
            'physical_dmg': 5 + self.enemy_lvl
        }
        self.enemy['current_hp_amount'] = self.enemy['max_hp_amount']

    def looper(self):
        while True:
            if self.combat is True:
                try:
                    self.new_turn()
                    action = int(input("Please enter your action:\n Attack: 1\n Heal: 2"))
                    self.end_turn()
                except ValueError:
                    print("Sorry, I didn't understand that.")
                    continue

                if action == 1:
                    self.my_attack()
                    self.enemy_attack()
                    continue
                elif action == 2:
                    self.enemy_attack()
                    self.my_heal()
                    continue
                # break

            if self.combat is False:
                if self.max_hp_amount_exp >= 100:
                    self.max_hp_amount_lvl += 1
                    self.max_hp_amount_exp -= 100
                if self.physical_dmg_exp >= 100:
                    self.physical_dmg_lvl += 1
                    self.physical_dmg_exp -= 100
                if self.max_mp_amount_exp >= 100:
                    self.max_mp_amount_lvl += 1
                    self.max_mp_amount_exp -= 100
                if self.mp_regen_exp >= 100:
                    self.mp_regen_lvl += 1
                    self.mp_regen_exp -= 100
                    self.player = {
                        'max_hp_amount': 100 + self.max_hp_amount_lvl,
                        'physical_dmg': 5 + self.physical_dmg_lvl,
                        'max_mp_amount': 20 + self.max_mp_amount_lvl,
                        'mp_regen': 1 + self.mp_regen_lvl,
                        'heal': 10 + self.hp_regen_lvl
                    }
                    self.player['current_hp_amount'] = self.player['max_hp_amount']
                    self.player['current_mp_amount'] = self.player['max_mp_amount']
                try:
                    option = int(input("Victory!\n Next enemy: 1"))
                except ValueError:
                    print("Sorry, I didn't understand that.")
                    continue

                if option == 1:
                    self.combat = True
                    continue
                # break

    def mp_regen(self):
        player = self.player
        if player.get('current_mp_amount') < player.get('max_mp_amount'):
            player['current_mp_amount'] = player.get('current_mp_amount') + player.get('mp_regen')
            self.mp_regen_exp = self.mp_regen_exp + player.get('mp_regen')

    def new_turn(self):
        self.mp_regen()
        print(
            f'Me: {self.player.get("current_hp_amount")}    Enemy Lvl {self.enemy_lvl}: {self.enemy.get("current_hp_amount")}\n'
            f'MP: {self.player.get("current_mp_amount")}')

    def end_turn(self):
        player = self.player
        enemy = self.enemy
        if enemy['current_hp_amount'] <= 0:
            self.enemy_lvl += 1
            self.enemy['current_hp_amount'] = 20 + self.enemy_lvl * 5
            self.enemy['physical_dmg'] = 5 + self.enemy_lvl
            print(
                f'You won!\n'
                f'Me: {player.get("current_hp_amount")}    Enemy Lvl {self.enemy_lvl}: {enemy.get("current_hp_amount")}\n'
                f'MP: {player.get("current_mp_amount")}')
            self.combat = False

    def enemy_attack(self):
        player = self.player
        enemy = self.enemy
        this_attack = random.randint(int(enemy.get('physical_dmg') * 0.7), int(enemy.get('physical_dmg') * 1.3))
        player['current_hp_amount'] = player.get('current_hp_amount') - this_attack
        print(f'Enemy attacked you for {this_attack} dmg')
        self.max_hp_amount_exp = self.max_hp_amount_exp + this_attack

    def my_attack(self):
        player = self.player
        enemy = self.enemy
        this_attack = random.randint(int(player.get('physical_dmg') * 0.7), int(player.get('physical_dmg') * 1.3))
        enemy['current_hp_amount'] = enemy.get('current_hp_amount') - this_attack
        print(f'You attacked enemy for {this_attack} dmg')
        self.physical_dmg_exp = self.physical_dmg_exp + this_attack

    def my_heal(self):
        player = self.player
        this_heal = random.randint(int(player.get('heal') * 1.8), int(player.get('heal') * 2.2))
        if player.get('current_mp_amount') >= player.get('heal'):
            if player.get('max_hp_amount') < this_heal + player.get('current_hp_amount'):
                player['current_hp_amount'] = player.get('max_hp_amount')
                player['current_mp_amount'] = player.get('current_mp_amount') - player.get('heal')
            else:
                player['current_hp_amount'] = this_heal + player.get('current_hp_amount')
                player['current_mp_amount'] = player.get('current_mp_amount') - player.get('heal')
            print(f'You healed yourself for {this_heal} HP')
            self.heal_exp = self.heal_exp + this_heal
        else:
            print('Not enough mana!')


RPGRunner().looper()
