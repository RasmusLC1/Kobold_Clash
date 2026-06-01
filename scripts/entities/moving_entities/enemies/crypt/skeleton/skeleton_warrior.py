from scripts.engine.keys.keys import keys
from scripts.entities.items.weapons.enemy_weapons.claw import Claw
from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton

import random


class Skeleton_Warrior(Skeleton):
    def __init__(self, game, pos):
        type = str(random.randint(1, 3))
        super().__init__(game, pos, keys.skeleton_warrior + '_' + type)
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.slash, 5)
