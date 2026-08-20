from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.engine.keys.keys import keys

import random


class Skeleton_Banner_Bearer(Skeleton):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.skeleton_banner_bearer)
        self.Equip_Weapon(Claw(self.game, self.pos))
        self.active_weapon.Set_Damage(keys.slash, 2)
        self.Set_Ability(keys.rally)


