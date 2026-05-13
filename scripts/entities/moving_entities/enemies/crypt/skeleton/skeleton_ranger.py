from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.ranged_weapons.bow import Bow
from scripts.engine.keys.keys import keys

import random


class Skeleton_Ranger(Skeleton):
    def __init__(self, game, pos):
        type = str(random.randint(1, 3))
        super().__init__(game, pos, keys.skeleton_ranger + '_' + type,  0, 3, 3)
        self.Equip_Weapon(Bow(self.game, self.pos))
        


    def Attack(self, delta_time):
        # If Player is to close, then archer cannot shoot
        if self.distance_to_player < 50:
            self.charge = 0
            return False
        
        super().Attack(delta_time)

    def Set_Attack_Triggered(self):
        self.Set_Target(self.game.player.pos)
        self.active_weapon.Enemy_Shooting()
        self.Reset_Charge()
        return True
