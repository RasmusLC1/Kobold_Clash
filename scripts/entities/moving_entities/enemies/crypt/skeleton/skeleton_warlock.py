from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.close_combat.staff import Staff
from scripts.engine.keys.keys import keys

import random


class Skeleton_Warlock(Skeleton):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.skeleton_warlock)
        self.Equip_Weapon(Staff(self.game, self.pos))
        
    def Equip_Weapon(self, weapon):
        super().Equip_Weapon(weapon)
        if self.active_weapon.sub_type == keys.fire_staff:
            self.Set_Behavior_Pattern(keys.medium_range)
        else:
            self.Set_Behavior_Pattern(keys.long_range)
