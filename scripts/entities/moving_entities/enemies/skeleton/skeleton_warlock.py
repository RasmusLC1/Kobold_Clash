from scripts.entities.moving_entities.enemies.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.ranged_weapons.bow import Bow
from scripts.engine.assets.keys import keys

import random


class Skeleton_Ranger(Skeleton):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.skeleton_warlock, health, strength, max_speed, agility, intelligence, stamina, 60)
        self.animation_handler.Set_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Cooldown_Max(100)
        self.animation_handler.Set_Animation_Num_Cooldown_Max(150)
        self.attack_distance  = 200
        self.attack_strategy = 'long_range'
        self.intent_manager.Set_Intent([ 'attack'])

        
        self.shooting_distance = False
        self.Equip_Weapon(Bow(self.game, self.pos))
        


    def Attack(self):
        if self.game.player.effects.invisibility.effect:
            return False
        
        if not self.active_weapon:
            return False

        if self.weapon_cooldown:
            return False
        
        # If Player is to close, then archer cannot shoot
        if self.distance_to_player < 50:
            return False

        self.Set_Target(self.game.player.pos)
        if self.active_weapon.type == keys.magic_staff:
            self.charge += 1
            self.active_weapon.Set_Charging_Enemy()
            if self.active_weapon.Enemy_Shooting():
                self.Reset_Charge()

                self.weapon_cooldown = 100
        
        return True
