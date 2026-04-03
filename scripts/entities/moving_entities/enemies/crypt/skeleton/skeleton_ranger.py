from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.ranged_weapons.bow import Bow
from scripts.engine.keys.keys import keys

import random


class Skeleton_Ranger(Skeleton):
    def __init__(self, game, pos):
        type = str(random.randint(1, 3))
        super().__init__(game, pos, keys.skeleton_ranger + '_' + type,  0, 3, 3, attack_speed = (0.9, 1.2), default_range=keys.long_range)
        self.attack_distance  = 200
        self.intent_manager.Set_Movement_Intent([ keys.long_range])

        
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
