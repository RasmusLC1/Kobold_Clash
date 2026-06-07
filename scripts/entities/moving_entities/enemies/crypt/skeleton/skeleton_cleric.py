from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.close_combat.sceptre import Sceptre
from scripts.engine.keys.keys import keys

import random


class Skeleton_Cleric(Skeleton):
    def __init__(self, game, pos):
        type = str(random.randint(1, 1))
        super().__init__(game, pos, keys.skeleton_cleric + '_' + type)
        self.Equip_Weapon(Sceptre(self.game, self.pos))

