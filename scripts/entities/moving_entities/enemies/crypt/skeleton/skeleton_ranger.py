from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.ranged_weapons.bow import Bow
from scripts.engine.keys.keys import keys

import random


class Skeleton_Ranger(Skeleton):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        type = str(random.randint(1, 3))
        super().__init__(game, pos, keys.skeleton_ranger + '_' + type, health, strength, max_speed, agility, intelligence, stamina, 1.2, 10)
        self.animation_handler.Set_Animation_Num_Max(3)
        self.animation_handler.Set_Attack_Animation_Num_Max(3)
        self.attack_distance  = 200
        self.attack_strategy = keys.long_range
        self.intent_manager.Set_Intent([ keys.attack])

        
        self.shooting_distance = False
        self.Equip_Weapon(Bow(self.game, self.pos))
        


    def Attack(self, delta_time):
        # If Player is to close, then archer cannot shoot
        if self.distance_to_player < 50:
            self.charge = 0
            return False
        
        super().Attack(delta_time)

    def Trigger_Attack(self):
        self.Set_Target(self.game.player.pos)
        self.active_weapon.Enemy_Shooting()
        self.Reset_Charge()
        return True
