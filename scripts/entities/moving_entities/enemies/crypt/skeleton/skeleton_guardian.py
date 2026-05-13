from scripts.entities.moving_entities.enemies.crypt.skeleton.skeleton import Skeleton
from scripts.entities.items.weapons.enemy_weapons.claw import Claw


import random
from scripts.engine.keys.keys import keys

class Skeleton_Guardian(Skeleton):
    def __init__(self, game, pos):
        super().__init__(game, pos, keys.skeleton_guardian)
        self.Equip_Weapon(Claw(game, self.pos)) 
        self.active_weapon.Set_Damage(keys.blunt, 5)


    def Set_Max_Charge(self):
        self.max_weapon_charge = 2 - self.active_weapon.speed / 10