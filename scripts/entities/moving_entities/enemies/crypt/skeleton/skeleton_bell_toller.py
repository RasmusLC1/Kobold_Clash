from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.engine.keys.keys import keys
from scripts.entities.items.weapons.enemy_weapons.claw import Claw

import random


class Skeleton_Bell_Toller(Skeleton):
    def __init__(self, game, pos):
        type = str(random.randint(1, 1))
        super().__init__(game, pos, keys.skeleton_bell_toller + '_' + type)
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.Set_Effect(keys.noisy_attacker, 10, True)