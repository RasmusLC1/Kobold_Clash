from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.close_combat.staff import Staff
from scripts.engine.keys.keys import keys

import random


class Skeleton_Warlock(Skeleton):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        super().__init__(game, pos, keys.skeleton_warlock, health, strength, max_speed, agility, intelligence, stamina, 1, 25)
        self.animation_handler.Set_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Max(4)
        self.animation_handler.Set_Attack_Animation_Num_Cooldown_Max(0.3)
        self.animation_handler.Set_Animation_Num_Cooldown_Max(1.2)
        self.attack_distance  = 200
        self.min_attack_range = 50
        self.attack_strategy = keys.long_range
        self.intent_manager.Set_Intent([ keys.attack])


        
        self.shooting_distance = False
        self.Equip_Weapon(Staff(self.game, self.pos))
        
    def Equip_Weapon(self, weapon):
        super().Equip_Weapon(weapon)

        if self.active_weapon.sub_type == keys.fire_staff:
            self.attack_distance  = 100
            self.min_attack_range = 30
            self.attack_strategy = keys.medium_range

    def Attack(self, delta_time):
        if self.game.player.effects.invisibility.effect:
            return False
        
        if not self.active_weapon:
            return False

        
        # If Player is to close, then archer cannot shoot
        if self.distance_to_player < self.min_attack_range:
            return False

        if "staff" in self.active_weapon.type:

            self.charge += delta_time
            self.active_weapon.Set_Charging_Enemy()
            if self.charge < self.max_weapon_charge:
                return False
            self.Set_Target(self.game.player.pos)
            self.game.particle_handler.Activate_Particles(random.randint(5, 10), keys.gold_particle, self.rect().center)
            
            self.active_weapon.Shoot_Projectiles()
            self.Reset_Charge()
        
        return True
