from scripts.engine.keys.keys import keys
from scripts.entities.items.weapons.enemy_weapons.claw import Claw

from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton

import random


class Skeleton_Warrior(Skeleton):
    def __init__(self, game, pos, health, strength, max_speed, agility, intelligence, stamina):
        type = str(random.randint(1, 3))
        super().__init__(game, pos, keys.skeleton_warrior + '_' + type, health, strength, max_speed, agility, intelligence, stamina, 0.8, 10)
        self.intent_manager.Set_Movement_Intent([keys.direct, keys.medium_range])
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.slash, 5)
