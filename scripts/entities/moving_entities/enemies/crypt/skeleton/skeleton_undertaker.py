from scripts.entities.items.weapons.close_combat.scythe import Scythe
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.engine.keys.keys import keys

import random


class Skeleton_Undertaker(Skeleton):
    def __init__(self, game, pos):
        type = str(random.randint(1, 1))
        super().__init__(game, pos, keys.skeleton_undertaker + '_' + type)
        self.Equip_Weapon(Scythe(self.game, self.pos))
        self.active_weapon.Set_Damage(keys.vampiric, 3)
        self.Set_Ability(keys.bone_ressurector)
