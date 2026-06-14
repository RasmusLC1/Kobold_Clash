from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.ranged_weapons.bow import Bow
from scripts.engine.keys.keys import keys

import random


class Skeleton_Ranger(Skeleton):
    def __init__(self, game, pos):
        type = str(random.randint(1, 3))
        super().__init__(game, pos, keys.skeleton_ranger + '_' + type)
        self.Equip_Weapon(Bow(self.game, self.pos))
        
